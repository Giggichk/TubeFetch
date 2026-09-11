import os
from tabulate import tabulate
from src.utils import get_browser_name
from src.validations import change_path, check_input, check_correct_link
from src.downloads import download, change_format
from src.formats import available_qualities


def main():
    ydl_opts = {
        "cookiesfrombrowser": (get_browser_name(),),
        "quiet": True,
    }

    url = check_correct_link()

    try:
        info = available_qualities(url, ydl_opts)
        print(tabulate(info, headers="keys", tablefmt="grid", showindex=True))

        format = check_input()

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

        path = input("Please specify the directory where you want to download the video: ")
        valid_path = change_path(path)

        if valid_path:
            full_output_template = os.path.join(str(valid_path), "%(title)s.%(ext)s")
            ydl_opts.setdefault("outtmpl", full_output_template)

            run = input("Do you want to run? (y/n): ").lower()
            if run == "y":
                download(url, ydl_opts)
                print("Video has been downloaded")

        else:
            print("Path is not valid")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()




