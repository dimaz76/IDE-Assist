#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main script entrypoint.
Авторы: [Ваше Имя]
Описание: Скрипт из ТЗ с поддержкой CSV, JSON и Excel; фильтрация по порогу; логирование; dry-run.
"""

import argparse
import logging
import sys
import os
import json
import yaml
import csv
import pandas as pd


def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Скрипт из ТЗ с поддержкой разных форматов и фильтром"
    )
    parser.add_argument(
        '-c','--config', required=True,
        help='Путь к файлу конфигурации (JSON или YAML)'
    )
    parser.add_argument(
        '-l','--log', choices=['DEBUG','INFO','WARNING','ERROR'],
        default='INFO', help='Уровень логирования'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Не сохранять файлы, только логировать'
    )
    return parser.parse_args()


def load_config(path):
    """Загрузка и валидация конфигурационного файла"""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Конфиг не найден: {path}")
    ext = os.path.splitext(path)[1].lower()
    with open(path, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f) if ext in ('.yaml','.yml') else json.load(f)
    # Проверка обязательных полей
    for key in ('input','output'):
        if key not in cfg:
            raise KeyError(f"В конфиге нет поля '{key}'")
    # Дефолтный порог фильтрации
    threshold = cfg.get('threshold', 10)
    # Проверяем тип порога
    if not isinstance(threshold, (int, float)):
        raise ValueError(f"Неверный порог фильтрации: {threshold}")
    return cfg['input'], cfg['output'], threshold


def load_data(path):
    """Загрузка данных из CSV, JSON или Excel"""
    logging.info(f"Загружаем данные из {path}")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Файл не найден: {path}")
    ext = os.path.splitext(path)[1].lower()
    if ext == '.csv':
        with open(path, newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    if ext == '.json':
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    if ext in ('.xls', '.xlsx'):
        df = pd.read_excel(path)
        return df.to_dict(orient='records')
    raise ValueError(f"Неподдерживаемый формат входа: {ext}")


def process_data(data, threshold):
    """Обработка данных: оставляем только записи с value > threshold"""
    logging.info(f"Обрабатываем данные, threshold={threshold}")
    filtered = []
    for row in data:
        try:
            if float(row.get('value', 0)) > threshold:
                filtered.append(row)
        except ValueError:
            logging.warning(f"Пропускаем некорректную запись: {row}")
    return filtered


def save_result(result, path, dry_run=False):
    """Сохранение результата в CSV, JSON или Excel"""
    logging.info(f"Сохраняем результат в {path}")
    if dry_run:
        logging.info("Dry-run: файл не сохраняем")
        return
    if not result:
        logging.warning("Нет данных для сохранения")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    ext = os.path.splitext(path)[1].lower()
    if ext == '.csv':
        with open(path, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=result[0].keys())
            w.writeheader(); w.writerows(result)
    elif ext == '.json':
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    elif ext in ('.xls', '.xlsx'):
        df = pd.DataFrame(result)
        df.to_excel(path, index=False)
    else:
        raise ValueError(f"Неподдерживаемый формат выхода: {ext}")


def main():
    args = parse_args()
    setup_logging(getattr(logging, args.log))
    logging.info(f"Уровень логирования: {args.log}")

    # вход, выход и порог из конфига
    try:
        input_path, output_path, threshold = load_config(args.config)
    except Exception:
        logging.exception("Ошибка при загрузке конфига")
        sys.exit(1)

    try:
        data = load_data(input_path)
        result = process_data(data, threshold)
        save_result(result, output_path, dry_run=args.dry_run)
    except Exception:
        logging.exception("Ошибка при выполнении сценария")
        sys.exit(1)

    logging.info("Готово!")

if __name__ == '__main__':
    main()