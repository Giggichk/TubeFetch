import re
import pathlib
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, ExtractorError


def check_correct_link():
    pattern = r"^(https?://)?(www\.)?(youtube\.com/(watch\?v=|shorts/)|youtu\.be/)[\w-]{11}"
    while True:
        try:
            url = input("Enter the link: ")
            if bool(re.match(pattern, url)):
                return url
            else:
                raise ValueError()
        except ValueError:
            print("Please enter a valid link")


def check_exist_link(url, options=None):
    opts = {
        'extract_flat': False,
        'quiet': True,
        'no_warnings': True,
        **(options or {})
    }

    with YoutubeDL(opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return True, "Supported link"
        except (ExtractorError, DownloadError) as error:
            clean_error = str(error).replace("ERROR: ", "").strip()
            return False, clean_error


def check_input():
    while True:
        try:
            return int(input("Please, enter the number: "))
        except ValueError:
            print("Please, enter a number")


def change_path(dir):
    if not dir or not str(dir).strip():
        return False

    raw_path = pathlib.Path(str(dir).strip()).expanduser()
    path = raw_path if raw_path.is_absolute() else (pathlib.Path.cwd() / raw_path)

    try:
        resolved_path = path.resolve(strict=False)
    except (RuntimeError, OSError):
        return False

    if resolved_path.exists() and resolved_path.is_dir():
        return resolved_path
    return False


def prompt_download_path():
    while True:
        path = input("📂 Укажите папку для скачивания: ").strip()
        valid_path = change_path(path)
        if valid_path:
            print(f"✅ Путь принят: {valid_path}")
            return valid_path
        print("❌ Неверный путь. Укажите существующую папку.")