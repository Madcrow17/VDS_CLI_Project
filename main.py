import os
from file_manager import FileManager


def main():
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
                main()
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
                main()
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
            while True:
                user_input = input(
                    "Введите команду (например, 'countfiles path_to_file_or_folder (Random_folders/...)') или 'back' для возврата в предыдущее меню > \n  ").strip()
                if user_input.lower() == "back":
                    print("Возврат в предыдущее меню")
                    main()
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
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверная команда, попробуйте ещё раз.")


if __name__ == "__main__":
    main()
