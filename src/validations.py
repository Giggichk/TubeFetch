import re
import os
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