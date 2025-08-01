import os
import shutil
import random


class FileManager:

    def __init__(self, base_dir=None):
        """
        Конструктор класса FileManager.

        Инициализирует экземпляр класса с базовой директорией для работы с файлами и папками.
        Если параметр `base_dir` не передан, устанавливает путь по умолчанию — папку "Random_folders"
        в текущей рабочей директории.

        :param base_dir: (str или None) - путь к базовой директории для файлового менеджера.
        """
        self.base_dir = os.path.join(os.getcwd(), "Random_folders")

    def __repr__(self):
        """
        Формирует официальное строковое представление объекта FileManager.

        :return: str — официальное строковое представление экземпляра.
        """
        return f"<FileManager base_dir='{self.base_dir}'>"

    def __str__(self):
        """
        Формирует удобочитаемое строковое представление объекта FileManager.

        :return: str — удобочитаемое описание экземпляра.
        """
        return f"Базовый путь для класса FileManager: {self.base_dir}"

    @staticmethod
    def random_name(words_list, count=2, separator=''):
        """
        Функция генерирует случайное название, состоящее из нескольких слов, выбранных из заданного списка.
        Случайным образом выбирается `count` слов из списка `words_list` с возможностью повторений.
        Выбранные слова объединяются в одну строку с помощью разделителя `separator`.

        :param words_list: список строк — слов, из которых выбираются элементы для формирования названия.
        :param count: целое число, количество слов для выбора (по умолчанию 2).
        :param separator: строка-разделитель для объединения выбранных слов (по умолчанию пустая строка).
        :return: name - сгенерированное название
        """

        selected_names = random.choices(words_list, k=count)
        name = separator.join(selected_names)
        return name

    @staticmethod
    def create_rand_file(path):
        """
        Функция создаёт файл с текстом по указанному пути `path` и заполняет его случайным текстом.
        Текст для заполнения генерируется с помощью метода `random_name` класса `FileManager`.
        В файл записывается строка из 10 случайных слов, выбранных из списка `FileManager.words_in_file`,
        объединённых пробелами.

        :param path: строка, путь к создаваемому файлу.
        :return: Метод не возвращает значения (None).
        """

        with open(path, 'w', encoding='utf-8') as f:
            f.write(FileManager.random_name(FileManager.words_in_file, count=10, separator=' '))

    @staticmethod
    def copy(src_path: str, dest_path: str) -> bool:
        """
        Функция копирует файл или папку из указанного пути src_path в dest_path.
        Если src_path — это файл, копируется одиночный файл.
        Если src_path — директория, копируется вся папка рекурсивно вместе с содержимым.
        Если dest_path уже существует и src_path — папка, копирование не происходит.

        :param src_path: Путь к исходному файлу или папке, которую нужно скопировать.
        :param dest_path: Путь к файлу или папке.
        :return: True, если копирование прошло успешно, иначе False.
        """

        try:
            if os.path.isfile(src_path):
                shutil.copy2(src_path, dest_path)  # Копирование файла
                print(f"Файл успешно скопирован: {src_path} -> {dest_path}")
            elif os.path.isdir(src_path):
                if os.path.exists(dest_path):
                    print(f"Папка назначения '{dest_path}' уже существует.")
                    return False
                shutil.copytree(src_path, dest_path)  # Копирование папки
                print(f"Содержимое папки успешно скопировано: {src_path} -> {dest_path}")
            else:
                print(f"Источник не существует: {src_path}")
                return False
            return True
        except Exception as e:
            print(f"Ошибка копирования: {e}")
            return False

    @staticmethod
    def delete(path: str) -> bool:
        """
        Функция удаляет файл или папку по указанному пути `path`
        Если `path` указывает на файл, файл удаляется.
        Если `path` указывает на папку, папка удаляется рекурсивно вместе со всем содержимым.
        Если путь не существует или не является ни файлом, ни папкой — выводится соответствующее сообщение.

        :param path: Путь к файлу или папке, которую необходимо удалить.
        :return: True, если удаление прошло успешно, иначе False.
        """
        if not os.path.exists(path):
            print(f"Путь '{path}' не найден.")
            return False

        try:
            if os.path.isfile(path):
                os.remove(path)
                print(f"Файл '{path}' успешно удалён.")
            elif os.path.isdir(path):
                shutil.rmtree(path)
                print(f"Папка '{path}' и её содержимое успешно удалены.")
            else:
                print(f"Путь '{path}' не является файлом или папкой.")
                return False
            return True
        except Exception as e:
            print(f"Ошибка при удалении '{path}': {e}")
            return False

    @staticmethod
    def make_random_filesystem(base_dir, max_depth=3, max_folders=3, max_files=4, current_depth=0):
        """
        Функция рекурсивно создаёт случайную файловую структуру с папками и файлами.
        Метод генерирует внутри заданной директории `base_dir` (Random_folders) случайное количество папок и файлов,
        при этом папки могут содержать вложенные папки и файлы, пока не будет достигнута глубина `max_depth`.

        Параметры позволяют задать максимальную глубину вложенности, а также лимиты на количество папок и файлов
        в одной директории.

        :param base_dir: str - путь к корневой директории, где начинается создание структуры.
        :param max_depth: int, optional (по умолчанию 3) - максимальная глубина вложенности папок, после которой рекурсия прекращается.
        :param max_folders: int, optional (по умолчанию 3) - максимальное количество папок, создаваемых в одной директории.
        :param max_files: int, optional (по умолчанию 4) - максимальное количество файлов, создаваемых в одной директории.
        :param current_depth: int, optional (по умолчанию 0) - Текущий уровень вложенности.

        :return: Меотод не возвращает значения (None).
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
            file_name = FileManager.random_name(FileManager.file_names, count=1) + "." + FileManager.random_name(
                FileManager.file_extensions, count=1)
            file_path = os.path.join(base_dir, file_name)
            FileManager.create_rand_file(file_path)
            print(f"Создан файл: {file_path}")

    @staticmethod
    def delete_random_filesystem(folder_path):
        """
        Функция удаляет папку и всё её содержимое по заданному пути `folder_path` (очистка случайной файловой структуры).

        Метод проверяет существование папки по пути `folder_path`.
        Если папка существует, выполняется рекурсивное удаление всей её структуры (включая все вложенные файлы и папки) с помощью `shutil.rmtree`.
        В случае успешного удаления выводится подтверждающее сообщение.
        Если возникает ошибка при удалении, выводится сообщение с описанием ошибки.
        Если папка не найдена, выводится соответствующее сообщение.

        :param folder_path: str - путь к папке, которую необходимо удалить вместе с её содержимым (Random_folders).
        :return: Метод не возвращает значения (None).
        """
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                print(f"Папка '{folder_path}' и содержимое успешно удалены.")
            except Exception as e:
                print(f"Ошибка при удалении папки: {e}")
        else:
            print(f"Папка '{folder_path}' не найдена.")

    @staticmethod
    def count_files(folder_path: str) -> int:
        """
        Функция подсчитывает количество файлов в папке и всех её вложенных папках.

        :param folder_path: Путь к папке для подсчёта файлов.
        :return: Общее число файлов (целое число).
        """
        if not os.path.exists(folder_path):
            print(f"Папка '{folder_path}' отсутствует. Путь не найден")
            return 0
        if not os.path.isdir(folder_path):
            print(f"'{folder_path}' не является папкой.")
            return 0

        file_count = 0
        for root, dirs, files in os.walk(folder_path):
            file_count += len(files)
        return file_count

    @staticmethod
    def print_menu():

        """
        Функция выводит интерактивное стартовое меню для пользовательского интерфейса CLI.

        Меню предлагает пользователю выбрать одно из действий:

        Этот метод не принимает аргументов и не возвращает значений.
        Он просто выводит текст меню в консоль.
        """

        print("\nВыберите действие:")
        print("1 - Создать дерево папок")
        print("2 - Удалить дерево папок")
        print("3 - Копирование файлов и папок (нажать для описания) ")
        print("4 - Удаление файлов и папок (нажать для описания) ")
        print("5 - Подсчет количества файлов в указанной папке")
        print("0 - Выход")

    """
    ________________ Случайные переменнтые ________________
    
    folder_names: список строк с именами папок.
    file_names: список строк с именами файлов.
    file_extensions: список строк с расширениями файлов.
    words_in_file: список слов для генерации содержимого файлов.
    """

    folder_names: list[str] = [
        "cache", "compiler", "debug", "encrypt", "exception",
        "function", "gateway", "interface", "kernel", "memory",
        "network", "node", "process", "server", "thread"
    ]

    file_names: list[str] = [
        "conf", "kernel", "bash", "shell", "daemon", "proc",
        "syslog", "init", "cron", "sudo", "apt",
        "grep", "chmod", "mkdir", "passwd", "tar",
        "ssh", "iptables", "fstab", "udev", "mount"
    ]

    file_extensions: list[str] = [
        "txt", "log", "cfg", "json", "xml"
    ]

    words_in_file: list[str] = [
        "algorithm", "array", "binary", "buffer", "byte",
        "cache", "compiler", "cookie", "data", "debug",
        "encrypt", "exception", "function", "gateway", "hash",
        "interface", "kernel", "loop", "memory", "network",
        "parameter", "process", "queue", "register", "runtime",
        "script", "server", "stack", "thread", "variable"
    ]
