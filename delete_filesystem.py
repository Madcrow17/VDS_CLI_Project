import shutil
import os

def delete_random_filesystem(folder_path):
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"Папка '{folder_path}' и содержимое успешно удалены.")
        except Exception as e:
            print(f"Ошибка при удалении папки: {e}")
    else:
        print(f"Папка '{folder_path}' не найдена.")


