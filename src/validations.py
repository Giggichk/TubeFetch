import re
import pathlib
import os


def check_correct_link():
    pattern = r"^(https?://)?(www\.)?(youtube\.com/(watch\?v=|shorts/)|youtu\.be/)[\w-]{11}"
    while True:
        try:
            url = input("Введите ссылку с YouTube на видео ➡️: ")
            if bool(re.match(pattern, url)):
                return url
            else:
                raise ValueError()
        except ValueError:
            print("Пожалуйста, введите корректную ссылку ⚠️")


def check_input(max_len):
    while True:
        try:
            number = int(input("Введите желаемый формат для скачивания: "))
            if 0 <= number <= max_len - 1:
                return number
            else:
                raise ValueError()
        except ValueError:
            print("Выберите только доступные форматы ❌")


def change_path(dir):

    path = pathlib.Path(dir)

    if path.is_absolute():
        if path.is_dir() and path.exists():
            return path
        else:
            return False
    else:
        home_dir = pathlib.Path.home()
        current_project_dir = pathlib.Path.cwd()

        target_name = path.name

        for root, dirs, files in os.walk(home_dir):
            root_path = pathlib.Path(root)
            if current_project_dir in root_path.parents or root_path == current_project_dir:
                continue

            if target_name in dirs:
                potential_path = root_path / target_name

                if potential_path.match(f"*{path}"):
                    return potential_path.resolve()

        return False


def prompt_download_path():
    while True:
        path = input("📂 Укажите папку для скачивания: ").strip()
        valid_path = change_path(path)
        if valid_path:
            print(f"✅ Путь принят: {valid_path}")
            return valid_path
        print("❌ Неверный путь. Укажите существующую папку.")