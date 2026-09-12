import os
from tabulate import tabulate
from src.utils import get_browser_name
from src.validations import check_input, check_correct_link, prompt_download_path
from src.downloads import download, change_format
from src.formats import available_qualities


def main():
    print("🎬 TubeFetch CLI")
    print("=" * 40)

    ydl_opts = {
        "cookiesfrombrowser": (get_browser_name(),),
        "quiet": True,
    }

    url = check_correct_link()

    try:
        info = available_qualities(url, ydl_opts)
        if not info:
            print("❌ Не удалось получить доступные форматы.")
            return

        print("\n📺 Доступные форматы:")
        print(tabulate(info, headers="keys", tablefmt="rounded_grid", showindex=True))

        while True:
            format = check_input()
            if 0 <= format < len(info):
                break
            print(f"❌ Введите число от 0 до {len(info) - 1}")

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
        else:
            print("ℹ️ Скачивание отменено")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()



