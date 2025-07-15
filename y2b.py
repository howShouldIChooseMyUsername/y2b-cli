import argparse
from pathlib import Path
import yt_dlp
import sys
import datetime
import shutil
import time

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="y2b - YouTube mp3/mp4 downloader")
    parser.add_argument("-v", "--version", action="store_true", help="Show version and exit")

    group = parser.add_mutually_exclusive_group(required=False)  # 여기서 required=False로 바꿈
    group.add_argument("-mp3", action="store_true", help="Download audio as mp3")
    group.add_argument("-mp4", action="store_true", help="Download video as mp4")

    parser.add_argument("-p1080", action="store_true", help="Set mp4 video quality to 1080p (default)")
    parser.add_argument("-p720", action="store_true", help="Set mp4 video quality to 720p")
    parser.add_argument("-p480", action="store_true", help="Set mp4 video quality to 480p")
    parser.add_argument("-p360", action="store_true", help="Set mp4 video quality to 360p")

    parser.add_argument("url", nargs="?", help="YouTube video URL")

    return parser.parse_args()


def get_downloads_folder() -> Path:
    return Path.home() / "Downloads"

def move_file_to_today_folder(file_path: Path):
    today_folder = get_today_folder()
    if file_path.exists():
        destination = today_folder / file_path.name
        shutil.move(str(file_path), str(destination))
        print(f"Moved '{file_path.name}' to '{today_folder}'")

def get_today_folder() -> Path:
    downloads = get_downloads_folder()
    today_folder = downloads / datetime.date.today().strftime("%Y-%m-%d")
    if not today_folder.exists():
        today_folder.mkdir()
    return today_folder

def move_latest_file(extension, output_path):
    files = list(output_path.glob(f'*.{extension}'))
    if not files:
        print(f"No *.{extension} files found in {output_path}")
        return
    latest_file = max(files, key=lambda f: f.stat().st_ctime)
    move_file_to_today_folder(latest_file)

def choose_quality(args):
    if args.p1080:
        return "1080"
    if args.p720:
        return "720"
    if args.p480:
        return "480"
    if args.p360:
        return "360"
    return "1080"

def download_mp3(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_path / '%(title)s.%(ext)s'),  # %(ext)s는 mp3로 변환 후 자동 확장자
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': True,
        'merge_output_format': 'mp3',  # 여기도 명시하면 확실함
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    move_latest_file('mp3', output_path)  # mp3 함수에서
    


def download_mp4(url, output_path, quality):
    # aac 오디오 스트림만 선택하도록 필터 추가
    fmt = f"bestvideo[height<={quality}]+bestaudio[acodec^=aac]/best"
    ydl_opts = {
        'format': fmt,
        'outtmpl': str(output_path / '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': True,
        'merge_output_format': 'mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    move_latest_file('mp4', output_path)  # mp4 함수에서



def main():
    VERSION = "1.1.0"
    args = parse_args()

    if args.version:
        print(f"y2b version {VERSION}")
        return

    if not (args.mp3 or args.mp4):
        print("Error: Please specify either -mp3 or -mp4 option.")
        return

    if not args.url:
        print("Error: Please provide a YouTube video URL.")
        return

    downloads_folder = get_downloads_folder()
    if not downloads_folder.exists():
        print(f"Download folder not found: {downloads_folder}")
        return

    if args.mp3:
        print("Starting mp3 download...")
        download_mp3(args.url, downloads_folder)
    elif args.mp4:
        quality = choose_quality(args)
        print(f"Starting mp4 download with quality {quality}p...")
        download_mp4(args.url, downloads_folder, quality)

    print("Download complete!")


if __name__ == "__main__":
    main()
