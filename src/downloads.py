from yt_dlp import YoutubeDL


def download(url, options):
    with YoutubeDL(options) as ydl:
         try:
             ydl.download(url)
         except Exception as e:
             print(e)


def change_format(height, fps, ext, audio):
    return f'bv[height={height}][fps={fps}][ext={ext}]+ba[ext={audio}]'