import os
import shutil
import random
from typing import List
from typing import Optional
import re
import datetime


class FileManager:

    def __init__(self, base_dir=None):
        """
        Конструктор класса FileManager.

        Метод инициализирует экземпляр класса с базовой директорией для работы с файлами и папками.
        Если параметр `base_dir` не передан, устанавливает путь по умолчанию — папку "Random_folders"
        в текущей рабочей директории.

        :param base_dir: (str или None) - путь к базовой директории для файлового менеджера.
        """
        self.base_dir = os.path.join(os.getcwd(), "Random_folders")

    def __repr__(self):
        """
        Метод формирует официальное строковое представление объекта FileManager.

        :return: str — официальное строковое представление экземпляра.
        """
        return f"<FileManager base_dir='{self.base_dir}'>"

    def __str__(self):
        """
        Метод формирует удобочитаемое строковое представление объекта FileManager.

        :return: str — удобочитаемое описание экземпляра.
        """
        return f"Базовый путь для класса FileManager: {self.base_dir}"

    @staticmethod
    def random_name(words_list: str, count=2, separator='') -> str:
        """
        Метод генерирует случайное название, состоящее из нескольких слов, выбранных из заданного списка.
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
    def create_rand_file(path: str) -> None:
        """
        Метод создаёт файл с текстом по указанному пути `path` и заполняет его случайным текстом.
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
        Метод копирует файл или содержимое папки из указанного пути src_path в dest_path.
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

                # Не дает скопировать, если такая папка уже есть в системе
                # if os.path.exists(dest_path):
                #    print(f"Папка назначения '{dest_path}' уже существует.")
                #    return False

                shutil.copytree(src_path, dest_path, dirs_exist_ok=True)  # Копирование папки
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
        Метод удаляет файл или папку по указанному пути `path`
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
    def make_random_filesystem(path: str, max_depth=3, max_folders=3, max_files=4, current_depth=0) -> None:
        """
        Метод рекурсивно создаёт случайную файловую структуру с папками и файлами.
        Метод генерирует внутри заданной директории `base_dir` (Random_folders) случайное количество папок и файлов,
        при этом папки могут содержать вложенные папки и файлы, пока не будет достигнута глубина `max_depth`.

        Параметры позволяют задать максимальную глубину вложенности, а также лимиты на количество папок и файлов
        в одной директории.

        :param path: str - путь к директории, где начинается создание структуры.
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

        for folders in range(folders_count):
            folder_name = FileManager.random_name(FileManager.folder_names, count=1)
            folder_path = os.path.join(path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            print(f"Создана папка: {folder_path}")
            # Рекурсивно создаём структуру внутри папки
            FileManager.make_random_filesystem(folder_path, max_depth, max_folders, max_files, current_depth + 1)

        for files in range(files_count):
            file_name = FileManager.random_name(FileManager.file_names, count=1) + "." + FileManager.random_name(
                FileManager.file_extensions, count=1)
            file_path = os.path.join(path, file_name)
            FileManager.create_rand_file(file_path)
            print(f"Создан файл: {file_path}")

    @staticmethod
    def delete_random_filesystem(path: str) -> None:
        """
        Метод удаляет папку и всё её содержимое по заданному пути `folder_path` (очистка случайной файловой структуры).

        Метод проверяет существование папки по пути `folder_path`.
        Если папка существует, выполняется рекурсивное удаление всей её структуры (включая все вложенные файлы и папки) с помощью `shutil.rmtree`.
        В случае успешного удаления выводится подтверждающее сообщение.
        Если возникает ошибка при удалении, выводится сообщение с описанием ошибки.
        Если папка не найдена, выводится соответствующее сообщение.

        :param path: str - путь к папке, которую необходимо удалить вместе с её содержимым (Random_folders).
        :return: Метод не возвращает значения (None).
        """
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                print(f"Папка '{path}' и содержимое успешно удалены.")
            except Exception as e:
                print(f"Ошибка при удалении папки: {e}")
        else:
            print(f"Папка '{path}' не найдена.")

    @staticmethod
    def count_files(path: str) -> int:
        """
        Метод подсчитывает количество файлов в папке и всех её вложенных папках.

        :param path: Путь к папке для подсчёта файлов.
        :return: Общее число файлов (целое число).
        """
        if not os.path.exists(path):
            print(f"Папка '{path}' отсутствует. Путь не найден")
            return 0
        if not os.path.isdir(path):
            print(f"'{path}' не является папкой.")
            return 0

        file_count = 0
        for root, dirs, files in os.walk(path):
            file_count += len(files)
        return file_count

    @staticmethod
    def find_files_by_name(path: str, pattern: str) -> List[str]:
        """
        Метод ищет все файлы в папке и её подпапках, имена которых соответствуют регулярному выражению.

        :param path: Путь к папке для поиска.
        :param pattern: Строка регулярного выражения для фильтрации имён файлов.
        :return: Список путей к найденным файлам.
        """
        regex = re.compile(pattern)
        matched_files = []

        for root, dirs, files in os.walk(path):
            for filename in files:
                if regex.search(filename):  # если имя файла соответствует шаблону
                    matched_files.append(os.path.join(root, filename))

        return matched_files

    @staticmethod
    def add_date(path: str, recursive: Optional[bool] = False) -> None:
        """
        Метод добавляет дату создания файла в его имя.
        Если path — папка, модифицирует имена всех файлов в папке.
        Если recursive=True (в консоле указан ключ --recursive) — обрабатывает файлы рекурсивно во вложенных папках.
        Если файл уже содержит дату в названии, то он пропускается.

        :param path: Путь к файлу или папке.
        :param recursive: Флаг рекурсивного обхода директорий.
        :return: Метод не возвращает значения (None).
        """

        def process_file(path: str) -> None:
            """
            Метод добавляет дату создания в формате YYYY-MM-DD к имени файла или папки.

            Метод получает дату создания файла или папки по пути `file_path`, формирует из неё строку
            в формате 'YYYY-MM-DD' и добавляет эту дату в имя файла перед расширением.
            Если в имени файла уже присутствует дата в данном формате в конце имени (до расширения),
            переименование не происходит.

            Если новое имя файла с добавленной датой уже существует в той же папке,
            файл не переименовывается, чтобы избежать конфликта имён.

            :param path: Полный путь к файлу или папке, имя которого нужно изменить.
            :return: Метод не возвращает значения (None).
            """

            ctime = os.path.getctime(path)
            date_str = datetime.datetime.fromtimestamp(ctime).strftime('%Y-%m-%d')

            dir_name, file_name = os.path.split(path)
            name, ext = os.path.splitext(file_name)

            if re.search(r'_\d{4}-\d{2}-\d{2}$', name):
                print(f"Файл '{file_name}' уже содержит дату.")
                return

            new_name = f"{name}_{date_str}{ext}"
            new_path = os.path.join(dir_name, new_name)

            if new_path != path:
                if not os.path.exists(new_path):
                    os.rename(path, new_path)
                    print(f"Переименован: {path} -> {new_path}")
                else:
                    print(f"Файл с именем {new_name} уже существует. Пропускаем.")

        if os.path.isfile(path):
            process_file(path)
        elif os.path.isdir(path):
            if recursive:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        process_file(os.path.join(root, file))
            else:
                for file in os.listdir(path):
                    full_path = os.path.join(path, file)
                    if os.path.isfile(full_path):
                        process_file(full_path)
        else:
            print(f"Путь '{path}' не существует или не является файлом/папкой.")

    @staticmethod
    def format_size(size_bytes: int) -> str:
        """
        Метод преобразует размер в байтах в удобочитаемый строковый формат с единицами измерения.

        Метод последовательно делит размер на 1024 и выбирает наиболее подходящую единицу
        измерения из ['B', 'KB', 'MB', 'GB', 'TB'], чтобы представить размер в
        читаемом виде.

        :param size_bytes: Размер в байтах (целое число).
        :return: Строка с размером и единицей измерения, например, "1.5MB", "244.0KB".
        """
        for item in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f}{item}"
            size_bytes /= 1024
        return f"{size_bytes:.1f}PB"

    @staticmethod
    def get_folder_size(path: str) -> int:
        """
        Метод рекурсивно вычисляет общий размер всех файлов в папке и её подпапках.

        Обходит заданный каталог и все его вложенные папки, суммируя размеры файлов.
        Если файл является символической ссылкой, он игнорируется.

        :param path: Путь к папке, размер которой нужно вычислить.
        :return: Общий размер файлов в байтах (int).
        """
        total_size = 0
        for root, dirs, files in os.walk(path):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    if os.path.islink(fp):
                        continue
                    total_size += os.path.getsize(fp)
                except (FileNotFoundError, PermissionError, OSError):
                    pass
        return total_size

    @staticmethod
    def analyse(path: str = '.') -> None:
        """
        Метод анализирует содержимое указанной папки на верхнем уровне и выводит в консоль информацию
        о размере всех файлов и подпапок в ней, а также общий размер папки.

        Вычисляет полный размер папки `folder_path` рекурсивно, используя
        вспомогательный метод `get_folder_size`. Затем получает список всех файлов и подпапок
        на первом уровне вложенности, определяет размер для каждого элемента, сортирует элементы по размеру в порядке убывания
        и выводит результат в удобочитаемом формате.

        При возникновении ошибок доступа к файлам или папкам размер считается равным 0.

        :param path: Путь к анализируемой папке.
        :return: Метод не возвращает значения (None).
        """
        folder_path = os.path.abspath(path)
        total_size = FileManager.get_folder_size(folder_path)

        entries = []
        with os.scandir(folder_path) as it:
            for entry in it:
                try:
                    if entry.is_file(follow_symlinks=False):
                        size = entry.stat().st_size
                    elif entry.is_dir(follow_symlinks=False):
                        size = FileManager.get_folder_size(entry.path)
                    else:
                        size = 0
                    entries.append((entry.name, size, entry.is_dir()))
                except (FileNotFoundError, PermissionError, OSError):
                    entries.append((entry.name, 0, entry.is_dir()))

        entries.sort(key=lambda x: x[1], reverse=True)

        print(f"> full size: {FileManager.format_size(total_size)}")
        for name, size, is_dir in entries:
            prefix = '- '
            if is_dir:
                display_name = f"{name}/"
            else:
                display_name = name

            spacing = ' ' * (20 - len(display_name)) if len(display_name) < 20 else ' '
            print(f"> {prefix}{display_name}{spacing}{FileManager.format_size(size)}")

    @staticmethod
    def print_help(less: bool = False) -> None:
        """
        Метод выводит в консоль справочную информацию по функционалу программы.
        """

        if less:
            help_text = """
                        ================== Справочная информация по программе ==================

                                        Это простая программа управления файлами

                            create-tree         Создать случайную файловую структуру в заданной папке в базовой директории программы
                            delete-tree         Удаляет случайную файловую структуру в заданной папке в базовой директории программы
                            copy                Копирует файл или папку из указанного пути 'src_path' в 'dest_path'
                            delete              Удаляет файл или папку по указанному пути 'path'
                            count               Подсчитывает количество файлов в папке 'path' и всех её вложенных папках
                            find                Ищет все файлы в папке 'path' и её подпапках, имена которых соответствуют 
                                                регулярному выражению 'pattern'
                            date                Добавляет дату создания файла в его имя по указанному пути 'path'
                            structure           Анализирует содержимое указанной папки по указанному пути 'path' на верхнем уровне 
                                                и выводит в консоль информацию о размере всех файлов и подпапок в ней, а также 
                                                общий размер папки
                            help                Выводит эту справочную информацию по программе
                            interface           Открывает интерфейс (меню с возможностью выбора) программы в CLI

                        ========================================================================
                        """
            print(help_text)

        else:
            help_text = """
            ================== Справочная информация по программе ==================

                            Это простая программа управления файлами

            Программа может принимать следующие позициональные аргументы:

              {create-tree,  delete-tree,  copy,  delete,  count,  find,  date,
               structure,  help,  interface}

                create-tree         Создать случайную файловую структуру в заданной папке в базовой директории программы
                delete-tree         Удаляет случайную файловую структуру в заданной папке в базовой директории программы
                copy                Копирует файл или папку из указанного пути 'src_path' в 'dest_path'
                delete              Удаляет файл или папку по указанному пути 'path'
                count               Подсчитывает количество файлов в папке 'path' и всех её вложенных папках
                find                Ищет все файлы в папке 'path' и её подпапках, имена которых соответствуют 
                                    регулярному выражению 'pattern'
                date                Добавляет дату создания файла в его имя по указанному пути 'path'
                structure           Анализирует содержимое указанной папки по указанному пути 'path' на верхнем уровне 
                                    и выводит в консоль информацию о размере всех файлов и подпапок в ней, а также 
                                    общий размер папки
                help                Выводит эту справочную информацию по программе
                interface           Открывает интерфейс (меню с возможностью выбора) программы в CLI

            Дополнительные опции:
              Для команды date:
                 --recursive           Рекурсивное добавление даты в название файлов в подпапках указанной папки

              Для команды create-tree:
                 --max-depth           Максимальная глубина вложенности папок (стандартно - 3)
                 --max-folders         Максимальное количество папок в директории (стандартно -3)
                 --max-files           Максимальное количество файлов в директории (стандартно - 4)

              -h, --help               Помощь по командам, можно применять к любой команде (аргументы)



            ========================================================================
            """
            print(help_text)

    @staticmethod
    def print_menu():

        """
        Метод выводит интерактивное стартовое меню для пользовательского интерфейса CLI.

        Меню предлагает пользователю выбрать одно из действий:

        Этот метод не принимает аргументов и не возвращает значений.
        Он просто выводит текст меню в консоль.
        """

        print("\nВыберите действие:")
        print("1 - Создание дерева папок в корневой директории (для теста)")
        print("2 - Удаление дерева папок из корневой директории (для теста)")
        print("3 - Копирование файлов и папок")
        print("4 - Удаление файлов и папок")
        print("5 - Подсчет количества файлов в указанной папке")
        print("6 - Поиск файлов по регулярному выражению")
        print("7 - Добавление к названию файла даты его создания (для папок может работать рекурсивно)")
        print("8 - Анализ фаловой системы и вывод размеров файлов и папок")
        print("9 - Вызов справки по программе")
        print("0 - Выход из программы")

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
