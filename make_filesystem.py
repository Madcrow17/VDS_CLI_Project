import os
import random


def random_name(words_list, count=2, separator=''):
    """Генерация случайного названия из заранее заданного списка"""

    selected_names = random.choices(words_list, k=count)
    name = separator.join(selected_names)
    return name


def create_rand_file(path):
    """Генерация текста для наполнения фалов"""

    with open(path, 'w', encoding='utf-8') as f:
        f.write(random_name(words_in_file, count=10, separator=' '))


def make_random_filesystem(base_path, max_depth=3, max_folders=3, max_files=4, current_depth=0):
    """
    Функция создаёт структуру из папок и файлов (случайным образом и случайным размером).

    - base_path: корень для создания (Random_files)
    - max_depth: максимальная глубина вложенности
    - max_folders: максимум папок в одной директории
    - max_files: максимум файлов в одной директории
    - current_depth: текущий уровень вложенности
    """

    if current_depth >= max_depth:
        return

    folders_count = random.randint(1, max_folders)
    files_count = random.randint(1, max_files)

    # Создание различных папок
    for folders in range(folders_count):
        folder_name = random_name(folder_names, count=1)
        folder_path = os.path.join(base_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Создана папка: {folder_path}")
        # Рекурсивно создаём структуру внутри папки
        make_random_filesystem(folder_path, max_depth, max_folders, max_files, current_depth + 1)

    # Создание различных файлов с различными расширениями
    for files in range(files_count):
        file_name = random_name(file_names, count=1) + "." + random_name(file_extensions, count=1)
        file_path = os.path.join(base_path, file_name)
        create_rand_file(file_path)
        print(f"Создан файл: {file_path}")


folder_names = [
    "cache", "compiler", "debug", "encrypt", "exception",
    "function", "gateway", "interface", "kernel", "memory",
    "network", "node", "process", "server", "thread"
]
file_names = [
    "conf", "kernel", "bash", "shell", "daemon", "proc",
    "syslog", "init", "cron", "sudo", "apt",
    "grep", "chmod", "mkdir", "passwd", "tar",
    "ssh", "iptables", "fstab", "udev", "mount"
]
file_extensions = [
    "txt", "log", "cfg", "json", "xml"
]
words_in_file = [
    "algorithm", "array", "binary", "buffer", "byte",
    "cache", "compiler", "cookie", "data", "debug",
    "encrypt", "exception", "function", "gateway", "hash",
    "interface", "kernel", "loop", "memory", "network",
    "parameter", "process", "queue", "register", "runtime",
    "script", "server", "stack", "thread", "variable"
]
