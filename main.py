import argparse
import os
from file_manager import FileManager
from cli_interface import cli_interface


def main():
    parser = argparse.ArgumentParser(description="Программа управления файлами")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Команда create-tree
    create_tree_pars = subparsers.add_parser('create-tree',
                                             help='Создает случайную файловую структуру в заданной папке в базовой директории программы',
                                             description='Создает случайную файловую структуру в заданной папке в базовой директории программы')

    create_tree_pars.add_argument('--max-depth', type=int, default=3,
                                  help='Максимальная глубина вложенности папок (стандартно - 3)')
    create_tree_pars.add_argument('--max-folders', type=int, default=3,
                                  help='Максимальное количество папок в директории (стандартно -3)')
    create_tree_pars.add_argument('--max-files', type=int, default=4,
                                  help='Максимальное количество файлов в директории (стандартно - 4)')
    create_tree_pars.add_argument('path', type=str, nargs='?', default='Random_folders', help='Путь к директории')

    # Команда delete-tree
    delete_tree_pars = subparsers.add_parser('delete-tree',
                                             help='Удаляет случайную файловую структуру в заданной папке в базовой директории программы',
                                             description='Удаляет случайную файловую структуру в заданной папке в базовой директории программы')

    delete_tree_pars.add_argument('path', type=str, nargs='?', default='Random_folders/', help='Путь к директории')

    # Команда copy
    copy_pars = subparsers.add_parser('copy', help='Копирует файл или папку из указанного пути src_path в dest_path',
                                      description='Копирует файл или папку из указанного пути src_path в dest_path')

    copy_pars.add_argument('src_path', type=str, nargs='?', help='Путь к источнику копирования')
    copy_pars.add_argument('dest_path', type=str, nargs='?', help='Место назначения')

    # Команда delete
    delete_pars = subparsers.add_parser('delete', help='Удаляет файл или папку по указанному пути path',
                                        description='Удаляет файл или папку по указанному пути path')

    delete_pars.add_argument('path', type=str, nargs='?', help='Путь к директории')

    # Команда count
    count_pars = subparsers.add_parser('count',
                                       help='Подсчитывает количество файлов в папке path и всех её вложенных папках',
                                       description='Подсчитывает количество файлов в папке path и всех её вложенных папках')

    count_pars.add_argument('path', type=str, nargs='?', help='Путь к директории')

    # Команда find
    find_pars = subparsers.add_parser('find',
                                      help='Ищет все файлы в папке path и её подпапках, имена которых соответствуют регулярному выражению',
                                      description='Ищет все файлы в папке path и её подпапках, имена которых соответствуют регулярному выражению')

    find_pars.add_argument('path', type=str, nargs='?', help='Путь к директории')
    find_pars.add_argument('pattern', type=str, nargs='?', default='',
                           help='Регулярное выражение для поиска фалов по нему')

    # Команда date
    date_pars = subparsers.add_parser('date', help='Добавляет дату создания файла в его имя',
                                      description='Добавляет дату создания файла в его имя')

    date_pars.add_argument('path', type=str, nargs='?', default='Random_folders/', help='Путь к директории')
    date_pars.add_argument('--recursive', action='store_true',
                           help='Ключ, если нужно добавить дату в названия файлов во всех вложенных папках')

    # Команда structure
    structure_pars = subparsers.add_parser('structure',
                                           help='Анализирует содержимое указанной папки folder_path на верхнем уровне и выводит в консоль информацию о размере всех файлов и подпапок в ней, а также общий размер папки',
                                           description='Анализирует содержимое указанной папки folder_path на верхнем уровне и выводит в консоль информацию о размере всех файлов и подпапок в ней, а также общий размер папки')

    structure_pars.add_argument('path', type=str, nargs='?', help='Путь к директории')

    # Команда help
    help_pars = subparsers.add_parser('manual', help='Выводит справочную информацию по программе',
                                      description='Выводит справочную информацию по программе')
    help_pars.add_argument('--less', default=None, action='store_true', help='Короткий вариант справочной информации')

    # Команда interface
    interface_pars = subparsers.add_parser('interface', help='Открывает интерфейс программы в CLI',
                                           description='Открывает интерфейс программы в CLI')

    args = parser.parse_args()

    if args.command == 'create-tree':
        FileManager.make_random_filesystem(
            path=args.path,
            max_depth=args.max_depth,
            max_folders=args.max_folders,
            max_files=args.max_files,
            current_depth=0,
        )

    if args.command == 'delete-tree':
        FileManager.delete_random_filesystem(
            path=args.path,
        )

    if args.command == 'copy':

        if not args.src_path and args.dest_path:
            print("Ошибка: не указаны папки источника и назначения.")
        elif not args.src_path:
            print("Ошибка: не указана папка источника.")
        elif not args.dest_path:
            print("Ошибка: не указана папка назначения.")
        else:
            FileManager.copy(
                src_path=args.src_path,
                dest_path=args.dest_path,
            )

    if args.command == 'delete':
        if not args.path:
            print("Ошибка: не указана папка или файл для удаления.")
        elif not os.path.exists(args.path):
            print(f"Такой папки: '{args.path}' не существует.")
        else:
            FileManager.delete(
                path=args.path,
            )

    if args.command == 'count':
        if not args.path:
            print("Ошибка: не указана папка для поиска.")
        elif not os.path.exists(args.path) or not os.path.isdir(args.path):
            print(f"Такой папки: '{args.path}' не существует.")
        else:
            count = FileManager.count_files(path=args.path)
            print(f"Количество файлов в папке (и ее подпапках) '{args.path}': {count}")

    if args.command == 'find':
        if not args.path:
            print("Ошибка: не указана папка для поиска.")
        elif not os.path.exists(args.path) or not os.path.isdir(args.path):
            print(f"Такой папки: '{args.path}' не существует.")
        elif not args.pattern:
            print("Ошибка: необходимо указать паттерн для команды find.")
        else:
            result_files = FileManager.find_files_by_name(path=args.path, pattern=args.pattern)
            print(f"Всего найдено {len(result_files)} файлов:")
            for file_path in result_files:
                print(file_path)

    if args.command == 'date':

        if not args.path:
            print("Ошибка: не указана папка для поиска.")
        elif not os.path.exists(args.path) or not os.path.isdir(args.path):
            print(f"Такой папки: '{args.path}' не существует.")
        else:
            FileManager.add_date(
                path=args.path,
                recursive=args.recursive
            )

    if args.command == 'structure':

        if not args.path:
            print("Ошибка: не указана папка для поиска.")
        elif not os.path.exists(args.path) or not os.path.isdir(args.path):
            print(f"Такой папки: '{args.path}' не существует.")
        else:
            FileManager.analyse(
                path=args.path,
            )

    if args.command == 'manual':
        FileManager.print_help(
            less=args.less
        )

    if args.command == 'interface':
        cli_interface()


if __name__ == "__main__":
    main()
