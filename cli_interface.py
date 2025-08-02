import os
from file_manager import FileManager


def cli_interface():
    """
    CLI интерфейс с меню, позволяющий выбирать действия.
    """

    while True:
        FileManager.print_menu()
        choice = input("Введите номер действия: ").strip()

        if choice == '1':
            # Создание дерева папок
            path = input("Введите путь для создания дерева папок (по умолчанию 'Random_folders'): ").strip()
            if not path:
                path = "Random_folders"
            try:
                max_depth = int(input("Максимальная глубина (по умолчанию 3): ").strip() or 3)
                max_folders = int(input("Максимальное количество папок (по умолчанию 3): ").strip() or 3)
                max_files = int(input("Максимальное количество файлов (по умолчанию 4): ").strip() or 4)
            except ValueError:
                print("Ошибка: Введены неверные числовые значения.")
                continue
            FileManager.make_random_filesystem(
                path=path,
                max_depth=max_depth,
                max_folders=max_folders,
                max_files=max_files,
                current_depth=0
            )

        elif choice == '2':
            # Удаление дерева папок
            path = input("Введите путь для удаления дерева папок (по умолчанию 'Random_folders'): ").strip()
            if not path:
                path = "Random_folders"
            FileManager.delete_random_filesystem(path=path)

        elif choice == '3':
            # Копирование
            src_path = input("Введите путь источника (файл или папка): ").strip()
            dest_path = input("Введите путь назначения: ").strip()
            if not src_path and not dest_path:
                print("Ошибка: не указаны папки источника и назначения.")
            elif not src_path:
                print("Ошибка: не указан путь источника.")
            elif not dest_path:
                print("Ошибка: не указан путь назначения.")
            else:
                FileManager.copy(src_path=src_path, dest_path=dest_path)

        elif choice == '4':
            # Удаление файла или папки
            path = input("Введите путь файла или папки для удаления: ").strip()
            if not path:
                print("Ошибка: путь не указан.")
            elif not os.path.exists(path):
                print(f"Путь '{path}' не существует.")
            else:
                FileManager.delete(path=path)

        elif choice == '5':
            # Подсчёт количества файлов
            path = input("Введите путь к папке для подсчёта файлов: ").strip()
            if not path:
                print("Ошибка: путь не указан.")
            elif not os.path.exists(path) or not os.path.isdir(path):
                print(f"Путь '{path}' не существует или не является директорией.")
            else:
                count = FileManager.count_files(path=path)
                print(f"Количество файлов в папке (и её подпапках) '{path}': {count}")

        elif choice == '6':
            # Поиск файлов по регулярному выражению
            path = input("Введите путь к папке для поиска файлов: ").strip()
            pattern = input("Введите выражение для поиска файлов: ").strip()
            if not path:
                print("Ошибка: путь не указан.")
            elif not os.path.exists(path) or not os.path.isdir(path):
                print(f"Путь '{path}' не существует или не является директорией.")
            elif not pattern:
                print("Ошибка: не указан паттерн поиска.")
            else:
                matched_files = FileManager.find_files_by_name(path=path, pattern=pattern)
                print(f"Найдено файлов: {len(matched_files)}")
                for file_path in matched_files:
                    print(file_path)

        elif choice == '7':
            # Добавление даты создания в название файла
            path = input("Введите путь файла или папки: ").strip()
            recursive_input = input("Рекурсивно добавить дату во все вложенные папки? (да/нет): ").strip().lower()
            recursive = recursive_input in ('да', 'yes', 'y')
            if not path:
                print("Ошибка: путь не указан.")
            elif not os.path.exists(path):
                print(f"Путь '{path}' не существует.")
            else:
                FileManager.add_date(path=path, recursive=recursive)

        elif choice == '8':
            # Анализ файловой системы (структура)
            path = input("Введите путь к папке для анализа (по умолчанию текущая директория): ").strip()
            if not path:
                path = '.'
            if not os.path.exists(path) or not os.path.isdir(path):
                print(f"Путь '{path}' не существует или не является директорией.")
            else:
                FileManager.analyse(path=path)

        elif choice == '9':
            # Вывод справки
            brief = input("Короткий вариант справки? (да/нет): ").strip().lower()
            FileManager.print_help(less=(brief in ('да', 'yes', 'y')))

        elif choice == '0':
            # Выход из программы
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор. Пожалуйста, введите номер от 0 до 9.")


if __name__ == "__main__":
    cli_interface()
