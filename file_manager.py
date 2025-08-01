import os
import shutil
import random


class FileManager:

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

    def __init__(self, base_dir=None ):
        self.base_dir = os.path.join(os.getcwd(), "Random_folders")

    def __repr__(self):
        return f"<FileManager base_dir='{self.base_dir}'>"

    def __str__(self):
        return f"Базовый путь для класса FileManager: {self.base_dir}"

    @staticmethod
    def random_name(words_list, count=2, separator=''):
        """Генерация случайного названия из заранее заданного списка"""

        selected_names = random.choices(words_list, k=count)
        name = separator.join(selected_names)
        return name

    @staticmethod
    def create_rand_file(path):
        """Генерация текста для наполнения фалов"""

        with open(path, 'w', encoding='utf-8') as f:
            f.write(FileManager.random_name(FileManager.words_in_file, count=10, separator=' '))

    @staticmethod
    def make_random_filesystem(base_dir, max_depth=3, max_folders=3, max_files=4, current_depth=0):
        """
        Функция создаёт структуру из папок и файлов (случайным образом и случайным размером).

        - base_dir: корень для создания (Random_files)
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
            folder_name = FileManager.random_name(FileManager.folder_names, count=1)
            folder_path = os.path.join(base_dir, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            print(f"Создана папка: {folder_path}")
            # Рекурсивно создаём структуру внутри папки
            FileManager.make_random_filesystem(folder_path, max_depth, max_folders, max_files, current_depth + 1)

        # Создание различных файлов с различными расширениями
        for files in range(files_count):
            file_name = FileManager.random_name(FileManager.file_names, count=1) + "." + FileManager.random_name(FileManager.file_extensions, count=1)
            file_path = os.path.join(base_dir, file_name)
            FileManager.create_rand_file(file_path)
            print(f"Создан файл: {file_path}")

    @staticmethod
    def delete_random_filesystem(folder_path):
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                print(f"Папка '{folder_path}' и содержимое успешно удалены.")
            except Exception as e:
                print(f"Ошибка при удалении папки: {e}")
        else:
            print(f"Папка '{folder_path}' не найдена.")

    @staticmethod
    def print_menu():

        """
        Функция, задающая стартовое меню при запуске main.py в CLI
        """

        print("\nВыберите действие:")
        print("1 - Создать дерево папок")
        print("2 - Удалить дерево папок")
        print("0 - Выход")

