import os
from tabulate import tabulate
from src.utils import get_browser_name, get_ffmpeg
from src.validations import check_input, check_correct_link, prompt_download_path
from src.downloads import download, change_format
from src.formats import available_qualities


def main():
    os.system("cls" if os.name == "nt" else "clear")

    print(r""" .-') _              .-. .-')    ('-.                ('-.   .-') _             ('-. .-. 
(  OO) )             \  ( OO ) _(  OO)             _(  OO) (  OO) )           ( OO )  / 
/     '._ ,--. ,--.   ;-----.\(,------.   ,------.(,------./     '._  .-----. ,--. ,--. 
|'--...__)|  | |  |   | .-.  | |  .---'('-| _.---' |  .---'|'--...__)'  .--./ |  | |  | 
'--.  .--'|  | | .-') | '-' /_)|  |    (OO|(_\     |  |    '--.  .--'|  |('-. |   .|  | 
   |  |   |  |_|( OO )| .-. `.(|  '--. /  |  '--. (|  '--.    |  |  /_) |OO  )|       | 
   |  |   |  | | `-' /| |  \  ||  .--' \_)|  .--'  |  .--'    |  |  ||  |`-'| |  .-.  | 
   |  |  ('  '-'(_.-' | '--'  /|  `---.  \|  |_)   |  `---.   |  | (_'  '--'\ |  | |  | 
   `--'    `-----'    `------' `------'   `--'     `------'   `--'    `-----' `--' `--' """)
    print("=" * 87)
    try:
        base_path = os.path.join(get_ffmpeg(), 'ffmpeg.exe')
        ydl_opts = {
            "cookiesfrombrowser": (get_browser_name(),),
            'ffmpeg_location': base_path,
            "quiet": True,
        }
    except Exception:
        ydl_opts = {
            "cookiesfrombrowser": (get_browser_name(),),
            "quiet": True,
        }

    url = check_correct_link()

    info = available_qualities(url, ydl_opts)
    if not info:
        print("❌ Не удалось получить доступные форматы.")
        return

    print("\n📺 Доступные форматы:")
    print(tabulate(info, headers="keys", tablefmt="rounded_grid", showindex=True))

    format = check_input(len(info))

    if info[format]['ext'] == "mp4":
        ydl_opts.setdefault("format", change_format(info[format]["height"],
                                                    info[format]["fps"],
                                                    info[format]["ext"],
                                                    "m4a"))
    elif info[format]['ext'] == "webm":
        ydl_opts.setdefault("format", change_format(info[format]["height"],
                                                    info[format]["fps"],
                                                    info[format]["ext"],
                                                    "webm"))

    valid_path = prompt_download_path()
    full_output_template = os.path.join(str(valid_path), "%(title)s.%(ext)s")
    ydl_opts.setdefault("outtmpl", full_output_template)

    run = input("▶️ Начать скачивание? (y/n): ").strip().lower()
    if run == "y":
        download(url, ydl_opts)
        print("✅ Видео успешно скачано")
        while True:
            new_session = input("\nВам нужно скачать еще одно видео? (y/n): ").strip().lower()
            if new_session == "y":
                return True
            elif new_session == "n":
                return False
            else:
                print("Выберите только y или n")
    else:
        print("ℹ️ Скачивание отменено")

if __name__ == "__main__":
    while True:
        try:
            if not main():
                break
            else:
                pass
        except Exception as e:
            print(e)



