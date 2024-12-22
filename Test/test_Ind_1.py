#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.Individ.Ind_1 import print_tree, main

@pytest.fixture
def mock_os():
    """Фикстура для имитации структуры файловой системы."""
    with patch("os.listdir") as mock_listdir, \
         patch("os.path.isdir") as mock_isdir, \
         patch("os.path.getsize") as mock_getsize:
        yield mock_listdir, mock_isdir, mock_getsize

def test_print_tree_directories_only(mock_os):
    mock_listdir, mock_isdir, _ = mock_os
    mock_listdir.side_effect = lambda dir: ["subdir1", "subdir2"] if dir == "." else []
    mock_isdir.side_effect = lambda path: True

    output = StringIO()
    with patch("sys.stdout", output):
        print_tree(".", show_files=False)
    result = output.getvalue().strip()
    expected = "├── subdir1\n├── subdir2"
    assert result == expected, f"Ожидалось:\n{expected}\nПолучено:\n{result}"

def test_print_tree_with_files_and_sizes(mock_os):
    mock_listdir, mock_isdir, mock_getsize = mock_os
    mock_listdir.side_effect = lambda dir: ["file1.txt", "file2.log"] if dir == "." else []
    mock_isdir.side_effect = lambda path: False
    mock_getsize.side_effect = lambda path: 100 if "file1.txt" in path else 200

    output = StringIO()
    with patch("sys.stdout", output):
        print_tree(".", show_files=True, show_size=True)
    result = output.getvalue().strip()
    expected = "├── file1.txt (100 bytes)\n├── file2.log (200 bytes)"
    assert result == expected, f"Ожидалось:\n{expected}\nПолучено:\n{result}"

def test_main_with_args():
    mock_args = [
        "script_name",  # Эмуляция имени скрипта
        ".",  # Каталог для отображения
        "-d", "2",  # Глубина
        "-f",  # Показывать файлы
        "-e", ".txt",  # Фильтр расширений
        "-s"  # Показывать размер
    ]

    with patch("sys.argv", mock_args), \
         patch("Prog.Individ.Ind_1.print_tree") as mock_print_tree:
        main()
    mock_print_tree.assert_called_once_with(
        ".",
        max_depth=2,
        show_files=True,
        filter_ext=".txt",
        show_size=True
    )
