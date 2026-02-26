#!/usr/bin/env python3
import subprocess
import sys
import os
import threading

try:
    from pync import Notifier
    HAS_PYNIC = True
except ImportError:
    HAS_PYNIC = False
    Notifier = None

DOWNLOAD_DIR = os.path.expanduser("~/Downloads")

def notify(title, message):
    if HAS_PYNIC:
        Notifier.notify(message, title=title)
    else:
        print(f"\a{title}: {message}")

def get_audio_quality():
    print("\nAudio Quality:")
    print("1. Best (320k)")
    print("2. High (256k)")
    print("3. Medium (128k)")
    print("4. Low (64k)")
    quality_map = {"1": "0", "2": "2", "3": "5", "4": "8"}
    choice = input("Select [1]: ").strip() or "1"
    return quality_map.get(choice, "0")

def get_video_quality():
    print("\nVideo Quality:")
    print("1. 1080p")
    print("2. 720p")
    print("3. 480p")
    print("4. 360p")
    print("5. Best available")
    quality_map = {"1": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
                   "2": "bestvideo[height<=720]+bestaudio/best[height<=720]",
                   "3": "bestvideo[height<=480]+bestaudio/best[height<=480]",
                   "4": "bestvideo[height<=360]+bestaudio/best[height<=360]",
                   "5": "bestvideo+bestaudio/best"}
    choice = input("Select [5]: ").strip() or "5"
    return quality_map.get(choice, "bestvideo+bestaudio/best")

def download_audio(url, quality):
    output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    cmd = [
        "yt-dlp",
        "-x", "--audio-format", "mp3",
        "--audio-quality", quality,
        "--embed-thumbnail",
        "--progress",
        "-o", output_template,
        url
    ]
    print(f"\nDownloading: {url}")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        notify("Download Complete", "Audio downloaded successfully!")
    return result.returncode

def download_video(url, quality):
    output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    cmd = [
        "yt-dlp",
        "-f", quality,
        "--merge-output-format", "mp4",
        "--progress",
        "-o", output_template,
        url
    ]
    print(f"\nDownloading: {url}")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        notify("Download Complete", "Video downloaded successfully!")
    return result.returncode

def parse_urls(input_str):
    urls = []
    for line in input_str.strip().split("\n"):
        line = line.strip()
        if line and not line.startswith("#"):
            if "," in line:
                urls.extend([u.strip() for u in line.split(",") if u.strip()])
            elif "http" in line:
                urls.append(line)
    return urls

def main():
    print("YouTube Downloader")
    print("=" * 30)
    print("1. Download Audio (MP3)")
    print("2. Download Video")
    print("3. Batch Download (from file)")
    print("q. Quit")
    print()
    
    choice = input("Select option: ").strip()
    
    if choice == "q":
        return
    
    if choice not in ("1", "2", "3"):
        print("Invalid option")
        sys.exit(1)
    
    if choice == "3":
        filepath = input("Enter path to text file (one URL per line): ").strip()
        if not os.path.exists(filepath):
            print("File not found")
            sys.exit(1)
        with open(filepath) as f:
            urls = parse_urls(f.read())
        if not urls:
            print("No URLs found in file")
            sys.exit(1)
        download_type = input("Download as audio? [y/N]: ").strip().lower() == "y"
        quality = get_audio_quality() if download_type else get_video_quality()
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] ", end="")
            if download_type:
                download_audio(url, quality)
            else:
                download_video(url, quality)
        notify("Batch Complete", f"Downloaded {len(urls)} files!")
        print("\nAll downloads complete!")
        return
    
    quality = get_audio_quality() if choice == "1" else get_video_quality()
    
    print("\nEnter URLs one at a time. Press Enter with empty line to download.")
    print("Type 'q' to quit.\n")
    
    while True:
        url = input("URL: ").strip()
        
        if url.lower() == "q":
            print("Done!")
            return
        
        if not url:
            continue
        
        print()
        i = 1
        if choice == "1":
            download_audio(url, quality)
        else:
            download_video(url, quality)
        
        print("\nReady for next URL (or 'q' to quit)")

if __name__ == "__main__":
    main()
