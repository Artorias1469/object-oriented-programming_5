#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse

def print_tree(directory, level=0, max_depth=None, show_files=True, filter_ext=None, show_size=False):
    """
    Рекурсивная функция для отображения дерева каталога.
    """
    if max_depth is not None and level >= max_depth:
        return

    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            # Отображение каталога
            if os.path.isdir(item_path):
                print("│   " * level + "├── " + item)
                print_tree(item_path, level + 1, max_depth, show_files, filter_ext, show_size)
            elif show_files and (filter_ext is None or item.endswith(filter_ext)):
                # Отображение файла
                if show_size:
                    size = os.path.getsize(item_path)
                    print(f"│   " * level + f"├── {item} ({size} bytes)")
                else:
                    print("│   " * level + "├── " + item)
    except PermissionError:
        print("│   " * level + "├── [Access Denied]")

def main():
    # Парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Показать структуру каталога в виде дерева.")
    parser.add_argument("directory", nargs="?", default=".", help="Каталог для отображения (по умолчанию текущий).")
    parser.add_argument("-d", "--max-depth", type=int, help="Максимальная глубина отображения каталога.")
    parser.add_argument("-f", "--files", action="store_true", help="Отображать файлы (по умолчанию только каталоги).")
    parser.add_argument("-e", "--extension", help="Фильтровать файлы по расширению (например, .txt).")
    parser.add_argument("-s", "--size", action="store_true", help="Отображать размер файлов.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Отображать дополнительную информацию.")
    args = parser.parse_args()

    # Дополнительная информация при включенном флаге verbose
    if args.verbose:
        print(f"Просмотр каталога: {args.directory}")
        if args.max_depth:
            print(f"Максимальная глубина: {args.max_depth}")
        if args.extension:
            print(f"Фильтр расширений: {args.extension}")
        if args.size:
            print("Размер файлов будет показан")

    print(args.directory)
    print_tree(
        args.directory,
        max_depth=args.max_depth,
        show_files=args.files,
        filter_ext=args.extension,
        show_size=args.size
    )

if __name__ == "__main__":
    main()
