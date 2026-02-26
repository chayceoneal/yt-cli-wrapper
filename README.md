# yt-cli-wrapper

A simple interactive CLI tool for downloading audio (MP3) or video from YouTube, built on top of [yt-dlp](https://github.com/yt-dlp/yt-dlp).

> I built this to help digitize videos from mine and my wife's childhood that we have on VHS but no longer have access to digitally — a quick way to download what you own but can't easily copy from the original source.

## Requirements

- Python 3
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg](https://ffmpeg.org/)

```bash
brew install yt-dlp ffmpeg
```

## Install

```bash
git clone https://github.com/yourusername/yt-cli-wrapper.git
cd yt-cli-wrapper
chmod +x yt-cli-wrapper.py
```

## Usage

```bash
./yt-cli-wrapper.py
```

You'll be prompted to choose a download mode:

| Option | Action |
|--------|--------|
| `1` | Download audio as MP3 |
| `2` | Download video |
| `3` | Batch download from a `.txt` file (one URL per line) |

After selecting a mode, choose your quality preference and paste in a URL — each download starts immediately. Type `q` to quit.

Downloaded files are saved to `~/Downloads/`.

## Optional: macOS Desktop Notifications

To receive a desktop notification when each download completes:

```bash
pip install pync
```

## License

MIT
