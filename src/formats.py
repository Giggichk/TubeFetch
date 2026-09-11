import json
from yt_dlp import YoutubeDL


def available_qualities(url, options=None):
    ydl_opts = {
        **(options or {}),
    }

    KEEP_KEYS = ["id", "formats"]
    KEEP_FORMATS_KEYS = ["ext", "height", "width", "fps"]
    seen = set()
    clean_formats = []
    result = []

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        clean_info = ydl.sanitize_info(info)

        filtered_info = {k: clean_info[k] for k in KEEP_KEYS if k in clean_info}

        if "formats" in filtered_info:
            for fmt in filtered_info['formats']:
                d = {k: fmt.get(k) for k in KEEP_FORMATS_KEYS}

                if None not in d.values():
                    clean_formats.append(d)

        for dict_info in clean_formats:
            str_d = json.dumps(dict_info, sort_keys=True)
            if str_d not in seen:
                seen.add(str_d)
                result.append(dict_info)

    return result


def print_qualities(clean_formats, index, choice):
    try:
        print(f"{choice}-ext:{clean_formats[index]['ext']}, height:{clean_formats[index]['height']}, fps:{clean_formats[index]['fps']}")
    except IndexError as err:
        print(err)


if __name__ == "__main__":
    lst = available_qualities("https://youtu.be/OTYIoEuKMmE?si=rgviYuPM7VvbsCD6", {"cookiesfrombrowser": ("firefox",)})
    print(lst)