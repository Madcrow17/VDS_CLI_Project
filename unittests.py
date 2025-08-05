import unittest
import os
import shutil
from file_manager import FileManager
from cli_interface import cli_interface
import re
from unittest import mock
import io


class TestFileManager(unittest.TestCase):
    test_dir = "test_folders/test/test"

    def setUp(self):
        # Метод запускается перед каждым тестом — можно подготавливать окружение
        self.test_dir = os.path.abspath(self.test_dir)
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def tearDown(self):
        # Метод запускается после каждого теста — удаляем созданные папки и файлы
        parent_dir = os.path.abspath(os.path.join(self.test_dir, ".."))
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

        if os.path.exists(parent_dir):
            shutil.rmtree(parent_dir)

    def test_01_make_random_filesystem(self):
        """
        Проверка на создание случайной файловой структуры, 3 теста с разными параметрами и путями для создания древа папок

        """

        print("\ntest_01_make_random_filesystem(self)\n")

        # Тестируем создание файловой структуры
        FileManager.make_random_filesystem(path=self.test_dir, max_depth=3, max_folders=2, max_files=2)

        # Проверяем, что папка создалась
        self.assertTrue(os.path.exists(self.test_dir))
        # Проверяем, что в папке есть что-то (файлы или папки)
        self.assertTrue(len(os.listdir(self.test_dir)) >= 0)

        print(f"Проверяем директорию: {self.test_dir}")
        print("Существует:", os.path.exists(self.test_dir))

        test_dir_1 = os.path.abspath(os.path.join(self.test_dir, "test1"))
        FileManager.make_random_filesystem(path=test_dir_1, max_depth=2, max_folders=1, max_files=0)

        self.assertTrue(os.path.exists(test_dir_1))
        self.assertTrue(len(os.listdir(test_dir_1)) >= 0)

        print(f"Проверяем директорию: {test_dir_1}")
        print("Существует:", os.path.exists(test_dir_1))

        test_dir_2 = os.path.abspath(os.path.join(self.test_dir, "../test2"))
        FileManager.make_random_filesystem(path=test_dir_2, max_depth=1, max_folders=3, max_files=10)

        self.assertTrue(os.path.exists(test_dir_2))
        self.assertTrue(len(os.listdir(test_dir_2)) > 0)

        print(f"Проверяем директорию: {test_dir_2}")
        print("Существует:", os.path.exists(test_dir_2))

    def test_02_delete_random_filesystem(self):
        """
        Проверка на удаление случайной файловой структуры

        """

        print("\ntest_02_delete_random_filesystem(self)\n")

        # Создание файловой структуры
        FileManager.make_random_filesystem(path=self.test_dir, max_depth=3, max_folders=2, max_files=3)

        # Проверяем, что папка создалась
        self.assertTrue(os.path.exists(self.test_dir))
        # Проверяем, что в папке есть что-то (файлы или папки)
        self.assertTrue(len(os.listdir(self.test_dir)) >= 0)

        # Вызываем метолд удаления случайной файловой структуры
        FileManager.delete_random_filesystem(self.test_dir)

        self.assertFalse(os.path.exists(self.test_dir))
        FileManager.delete_random_filesystem(self.test_dir)

    def test_03_count_files(self):
        """
        Проверяем метод подсчета количества файлов в папках\папке

        """

        print("\ntest_03_count_files(self)\n")

        test_dir_count_1 = os.path.abspath(os.path.join(self.test_dir, "test_count_1"))
        FileManager.make_random_filesystem(path=test_dir_count_1, max_depth=3, max_folders=3, max_files=5)

        count = FileManager.count_files(self.test_dir)
        max_files = 5 * (1 + 3 + 3 ** 2)

        self.assertTrue(count <= max_files)
        self.assertTrue(count > 0)

        print(f"Проверяем директорию: {test_dir_count_1}")
        print("Существует:", os.path.exists(test_dir_count_1))
        print(FileManager.count_files(test_dir_count_1), '<', max_files)
        print(FileManager.count_files(test_dir_count_1), '> 0')

        # Удаляем тестовую директорию
        shutil.rmtree(test_dir_count_1)

        test_dir_count_2 = os.path.abspath(os.path.join(self.test_dir, "test_count_2"))
        FileManager.make_random_filesystem(path=test_dir_count_2, max_depth=0, max_folders=0, max_files=0)

        print(f"Проверяем директорию: {test_dir_count_2}")
        print("Существует:", os.path.exists(test_dir_count_2))
        print("В директории: ", FileManager.count_files(test_dir_count_2), "файлов")

        self.assertTrue(os.path.exists(test_dir_count_2))
        # Проверяем, что созданы папки, но файлов нет
        for root, dirs, files in os.walk(test_dir_count_2):
            self.assertGreaterEqual(len(dirs), 0)
            self.assertEqual(len(files), 0)

    def test_04_find_files_by_name(self):
        """
        Проверяем метод поиска файлов по паттерну

        """

        print("\ntest_04_find_files_by_name(self)\n")

        # Создаём файлы с разными именами
        filenames = ["conf.cfg", "kernel.log", "bash.txt", "shell.sh", "daemon.txt", "proc.sh",
                     "syslog.conf", "init.d", "cron.conf", "sudo.sh", "apt.log",
                     "grep.sh", "chmod.d", "mkdir.cfg", "passwd.txt", "tar.conf",
                     "ssh.sh", "iptables.d", "fstab.d", "udev.txt", "mount.log"]
        for name in filenames:
            with open(os.path.join(self.test_dir, name), 'w') as f:
                f.write("content")

        result = FileManager.find_files_by_name(self.test_dir, r'.*\.txt$')
        print("\n".join(result))

        self.assertEqual(len(result), 4)
        self.assertTrue(all(f.endswith('.txt') for f in result))

        print("_______________________")

        result_1 = FileManager.find_files_by_name(self.test_dir, r'.*\.(log|txt)$')
        print("\n".join(result_1))

        self.assertEqual(len(result_1), 7)
        self.assertTrue(all(f.endswith('.log') or f.endswith('.txt') for f in result_1))

    def test_05_copy_file_and_directory(self):
        """
        Проверяем метод копирования файлов и содержимых папок

        """

        print("\ntest_05_test_copy_file_and_directory(self)\n")

        foldernames = ["cache", "memory", "syslog"]
        files_in_folders = {
            "cache": ["cron.txt", "varlog.log"],
            "memory": ["file.txt", "ssh.sh"],
            "syslog": ["fstable", "system.log"],
        }

        for folder in foldernames:
            folder_path = os.path.join(self.test_dir, folder)
            os.makedirs(folder_path, exist_ok=True)

            for filename in files_in_folders[folder]:
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("content")

        src_path = os.path.join(self.test_dir, 'cache/cron.txt')
        dest_path = os.path.join(self.test_dir, 'memory/cron.txt')
        dest_path_1 = os.path.join(self.test_dir, 'memory/')

        result = FileManager.copy(src_path, dest_path)
        print(FileManager.analyse(dest_path_1))

        self.assertTrue(result)
        self.assertTrue(os.path.isfile(dest_path))

        src_path = os.path.join(self.test_dir, 'cache/')
        dest_path = os.path.join(self.test_dir, 'syslog/')

        # Копируем содержимое папки
        result_1 = FileManager.copy(src_path, dest_path)
        print(FileManager.analyse(dest_path))
        print(result_1)

        self.assertTrue(result)
        self.assertTrue(os.path.isdir(dest_path))
        self.assertTrue(os.path.isfile(os.path.join(dest_path, 'varlog.log')))

    def test_06_delete(self):
        """
        Проверяем метод удаления отделных папок и файлов
        """

        print("\ntest_06_delete(self)\n")

        foldernames = ["cache", "memory", "syslog"]
        files_in_folders = {
            "cache": ["cron.txt", "varlog.log"],
            "memory": ["file.txt", "ssh.sh"],
            "syslog": ["fstable", "system.log"],
        }

        for folder in foldernames:
            folder_path = os.path.join(self.test_dir, folder)
            os.makedirs(folder_path, exist_ok=True)

            for filename in files_in_folders[folder]:
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("content")

        # Удаляем файл
        res_file = FileManager.delete(os.path.join(self.test_dir, 'cache/cron.txt'))
        print(res_file)

        self.assertTrue(res_file)
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, 'cache/cron.txt')))

        # Удаляем папку
        res_folder = FileManager.delete(os.path.join(self.test_dir, 'memory/'))
        print(res_file)
        print(FileManager.analyse(self.test_dir))

        self.assertTrue(res_folder)
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, 'memory/')))

    def test_07_add_date(self):
        """
        Проверяем метод добавления даты в название файла\файлов

        """

        print("\ntest_07_add_date(self)\n")

        filenames = ["cron.txt", "syslog.log", "ssh.sh", "fstables.dll"]

        for filename in filenames:
            file_path = os.path.join(self.test_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("content")

        # Добавляем дату
        FileManager.add_date(os.path.join(self.test_dir, 'cron.txt'))
        print(FileManager.analyse(self.test_dir))

        # Проверяем — должен появиться файл с датой в имени, а старый файл исчезнуть
        files = os.listdir(self.test_dir)
        self.assertTrue(any(re.search(r'cron_\d{4}-\d{2}-\d{2}\.txt$', f) for f in files))
        self.assertEqual(len(files), 4)

        FileManager.add_date(os.path.join(self.test_dir))
        print(FileManager.analyse(self.test_dir))

        files = os.listdir(self.test_dir)
        pattern = re.compile(r'.*_\d{4}-\d{2}-\d{2}\..+$')
        self.assertTrue(all(pattern.match(f) for f in files),
                        msg=f"Найдены файлы без даты в имени: {[f for f in files if not pattern.match(f)]}")
        self.assertEqual(len(files), 4)

    def test_08_analyse(self):
        """
        Проверяем метод анализа файловой структуры

        """

        print("\ntest_08_analyze(self)\n")

        foldernames = ["cache", "memory", "syslog"]
        files_in_folders = {
            "cache": ["cron.txt", "varlog.log"],
            "memory": ["file.txt", "ssh.sh"],
            "syslog": ["fstable", "system.log"],
        }

        for folder in foldernames:
            folder_path = os.path.join(self.test_dir, folder)
            os.makedirs(folder_path, exist_ok=True)

            for filename in files_in_folders[folder]:
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("content")

        filenames = ["cron.txt", "syslog.log", "ssh.sh", "fstables"]

        for filename in filenames:
            file_path = os.path.join(self.test_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("content")

        try:
            FileManager.analyse(self.test_dir)
        except Exception as e:
            self.fail(f"Analyse method raised an exception: {e}")

    def test_09_print_help(self):
        """
        Проверяем метод вывода справки о программе

        """

        print("\ntest_09_print_help(self)\n")

        # Проверяем, что метод print_help не падает и выводит что-то
        with mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            FileManager.print_help(less=False)
            output_full = mock_stdout.getvalue()
            self.assertIn("Программа может принимать", output_full)

        with mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            FileManager.print_help(less=True)
            output_short = mock_stdout.getvalue()
            self.assertIn("Это простая программа управления файлами", output_short)

    def test_10_cli_interface_exit(self):
        """
        Проверяем метод входа и быстрого выхода из интерфейса

        """

        print("\ntest_10_cli_interface_exit(self)\n")

        # Мокаем input чтобы сразу выбрать выход '0'
        with mock.patch('builtins.input', side_effect=['0']), \
                mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            cli_interface()
            output = mock_stdout.getvalue()
            self.assertIn("Выберите действие:", output)
            self.assertIn("Выход из программы.", output)

    def test_11_cli_interface_invalid_choice_then_exit(self):
        """
        Проверяем некорректный выбор пункта меню и выход из интерфейса

        """

        print("\ntest_11_cli_interface_invalid_choice_then_exit(self)\n")

        # Проверяем ввод некорректного выбора, потом выход
        with mock.patch('builtins.input', side_effect=['invalid', '0']), \
                mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            cli_interface()
            output = mock_stdout.getvalue()
            self.assertIn("Некорректный выбор", output)
            self.assertIn("Выход из программы.", output)


if __name__ == "__main__":
    unittest.main()
