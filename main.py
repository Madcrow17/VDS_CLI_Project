import os
from make_filesystem import make_random_filesystem
from delete_filesystem import delete_random_filesystem
from menu import print_menu


def main():
    while True:
        print_menu()
        choice = input("Введите номер команды: ").strip()

        if choice == "1":
            base_dir = os.path.join(os.getcwd(), "Random_folders")  # Текущая рабочая директория
            os.makedirs(base_dir, exist_ok=True)
            print(f"Генерация рандомной структуры в каталоге: {base_dir}")
            make_random_filesystem(base_dir)
        elif choice == "2":
            base_dir = os.path.join(os.getcwd(), "Random_folders")
            delete_random_filesystem(base_dir)
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод, попробуйте ещё раз.")


if __name__ == "__main__":
    main()
