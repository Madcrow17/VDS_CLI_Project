import os
from file_manager import FileManager


def cli_interface():
    while True:
        FileManager.print_menu()
        choice = input("Введите номер команды: ").strip()

        if choice == "1":
            base_dir = os.path.join(os.getcwd(), "Random_folders")  # Текущая рабочая директория
            os.makedirs(base_dir, exist_ok=True)
            print(f"Генерация случайных фалов и папок в каталоге: {base_dir}")
            FileManager.make_random_filesystem(base_dir)

        elif choice == "2":
            base_dir = os.path.join(os.getcwd(), "Random_folders")
            FileManager.delete_random_filesystem(base_dir)

        elif choice == "3":
            user_input = input(
                "Введите команду (например, 'copy Random_folders/source.extension Random_folders/destination') или 'back' для возврата в предыдущее меню > \n").strip()
            if user_input.lower() == "back":
                print("Возврат в предыдущее меню")
                cli_interface()
                break
            if not user_input:
                continue
            parts = user_input.split()
            if not parts:
                print("Введите команду заново")
            else:
                cmd_name = parts[0]
                cmd_args = parts[1:]
                if cmd_name == "copy":
                    if len(cmd_args) != 2:
                        print("Ошибка: команда copy требует 2 аргумента: источник и назначение")
                    else:
                        src, dest = cmd_args
                        FileManager.copy(src, dest)
                else:
                    print(f"Неизвестная команда: {cmd_name}")

        elif choice == "4":
            user_input = input(
                "Введите команду (например, 'delete path_to_file_or_folder (Random_folders/...)') или 'back' для возврата в предыдущее меню > \n ").strip()
            if user_input.lower() == "back":
                print("Возврат в предыдущее меню")
                cli_interface()
                break
            if not user_input:
                continue
            parts = user_input.split()
            if not parts:
                print("Введите команду заново")
                continue
            cmd_name = parts[0]
            cmd_args = parts[1:]
            if cmd_name == "delete":
                if len(cmd_args) != 1:
                    print("Ошибка: команда copy требует 1 аргумент: путь к файлу")
                    continue
                path = cmd_args[0]
                FileManager.delete(path)
            else:
                print(f"Неизвестная команда: {cmd_name}")

        elif choice == "5":
            user_input = input(
                "Введите команду (например, 'countfiles path_to_file_or_folder (Random_folders/...)') или 'back' для возврата в предыдущее меню > \n  ").strip()
            if user_input.lower() == "back":
                print("Возврат в предыдущее меню")
                cli_interface()
                break
            parts = user_input.split()
            if not parts:
                continue
            cmd_name = parts[0]
            cmd_args = parts[1:]
            if cmd_name == "countfiles":
                if len(cmd_args) != 1:
                    print("Ошибка: команда countfiles требует 1 аргумент — путь к папке")
                    continue
                path = cmd_args[0]
                count = FileManager.count_files(path)
                print(f"Количество файлов в папке '{path}': {count}")
            else:
                print(f"Неизвестная команда: {cmd_name}")

        elif choice == "6":
            user_input = input(
                "Введите команду (например, 'findfiles path_to_file_or_folder pattern или 'back' для возврата в предыдущее меню > \n  ").strip()
            if user_input.lower() == "back":
                print("Возврат в предыдущее меню")
                cli_interface()
                break
            parts = user_input.split()
            if not parts:
                continue
            cmd_name = parts[0]
            cmd_args = parts[1:]
            if cmd_name == "findfiles":
                if len(cmd_args) != 2:
                    print("Ошибка: команда countfiles требует 2 аргумента — путь к папке и паттерн для поиска")
                    continue
                path, pattern = cmd_args
                result_files = FileManager.find_files_by_name(path, pattern)
                print(f"Всего найдено {len(result_files)} файлов: ")
                for files in result_files:
                    print(files)
            else:
                print(f"Неизвестная команда: {cmd_name}")

        elif choice == "7":
            user_input = input(
                "Введите команду (например, 'date path_to_file_or_folder key [--recursive если объект является папкой]') или 'back' для возврата в предыдущее меню > \n  ").strip()
            if user_input.lower() == "back":
                print("Возврат в предыдущее меню")
                cli_interface()
                break
            parts = user_input.split()
            if not parts:
                continue
            cmd_name = parts[0]
            cmd_args = parts[1:]
            if cmd_name == "date":
                if 2 < len(cmd_args) < 1:
                    print(
                        "Ошибка: команда date используется следующим образом: 'date path_to_file_or_folder key (Если папка и ключ --recursive не указан, меняет имена только в заданной папке, если указан, то обходит все вложенные папки)'")
                    continue
                path = cmd_args[0]
                recursive_flag = '--recursive' in cmd_args
                FileManager.add_date(path, recursive_flag)
            else:
                print(f"Неизвестная команда: {cmd_name}")

        elif choice == "8":
            user_input = input(
                "Введите команду (например, 'structure path_to_file_or_folder (Random_folders/...)') или 'back' для возврата в предыдущее меню > \n  ").strip()
            if user_input.lower() == "back":
                print("Возврат в предыдущее меню")
                cli_interface()
                break
            parts = user_input.split()
            if not parts:
                continue
            cmd_name = parts[0]
            cmd_args = parts[1:]
            if cmd_name == "structure":
                if len(cmd_args) != 1:
                    print("Ошибка: команда structure требует 1 аргумент — путь к папке")
                    continue
                path = cmd_args[0]
                FileManager.analyse(path)
        elif choice == "9":
            FileManager.print_help(less=None)
            user_input = input(
                "Для возврата в предыдущее меню введите 'back'> \n  ").strip()
            if user_input.lower() == "back":
                print("Возврат в предыдущее меню")
                cli_interface()
                break

        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверная команда, попробуйте ещё раз.")
