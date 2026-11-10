# YouTube Downloader

A small command-line script that downloads a YouTube video as an **MP4 video**, an **MP3 audio file**, or **both**. It uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) under the hood.

> Only download videos you own or have permission to download.

## Requirements

- **Python 3.8+**
- **yt-dlp** (Python package)
- **FFmpeg**, needed to merge video and audio into an MP4 and to convert audio to MP3

## Setup (Windows)

1. **Open a terminal in this folder** (PowerShell):

   ```powershell
   cd "C:\Users\NO\Documents\youtube downloader"
   ```

2. **Create and activate a virtual environment** (skip creating it if `.venv` already exists):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks the activation script, run this once, then try again:

   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   ```

3. **Install yt-dlp:**

   ```powershell
   python -m pip install -U yt-dlp
   ```

4. **Install FFmpeg** (if you don't have it yet):

   ```powershell
   winget install Gyan.FFmpeg
   ```

   Close and reopen the terminal afterwards, then check it works with `ffmpeg -version`.

5. **Install Deno** (a JavaScript runtime yt-dlp needs for YouTube) and yt-dlp's extras:

   ```powershell
   winget install DenoLand.Deno
   python -m pip install -U "yt-dlp[default]"
   ```

   Reopen the terminal afterwards. Without this you'll see `No supported JavaScript runtime could be found` and some formats may be missing.

## Usage

```powershell
python download_youtube.py <URL> [-o OUTPUT_FOLDER] [-f {mp4,mp3,both}] [-p]
```

| Option | Description | Default |
| --- | --- | --- |
| `URL` | The YouTube video link (`youtube.com` or `youtu.be`) | required |
| `-o`, `--output` | Folder to save the file in (created if it doesn't exist) | current folder |
| `-f`, `--format` | `mp4` for video, `mp3` for audio only, or `both` | `mp4` |
| `-p`, `--playlist` | Download every video in the playlist | off (single video) |

### Examples

Download a video as MP4 into the current folder:

```powershell
python download_youtube.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Download audio only as MP3 into the `downloads` folder:

```powershell
python download_youtube.py "https://youtu.be/VIDEO_ID" -o downloads -f mp3
```

Download both the MP4 and an MP3:

```powershell
python download_youtube.py "https://www.youtube.com/watch?v=VIDEO_ID" -o downloads -f both
```

Download an entire playlist as MP3s:

```powershell
python download_youtube.py "https://www.youtube.com/playlist?list=PLAYLIST_ID" -o downloads -f mp3 --playlist
```

Show the built-in help:

```powershell
python download_youtube.py --help
```

Tip: put the URL in quotes so characters like `&` aren't interpreted by the shell.

## Notes

- Files are named after the video title, e.g. `My Video.mp4`.
- Without `--playlist`, only the single video is downloaded, even if the link points into a playlist.
- With `--playlist`:
  - Files keep the same naming (video title), saved directly in the output folder.
  - Private or deleted videos are skipped instead of stopping the download.
  - Finished videos are recorded in `_archive.txt` in the output folder. Re-running the same command resumes an interrupted download and only fetches new videos. Delete `_archive.txt` to download everything again.
- Best available quality is used.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `Missing dependency: yt-dlp` | Activate the virtual environment, then run `python -m pip install yt-dlp` |
| `please provide a valid YouTube URL` | Use a full link starting with `https://` from `youtube.com` or `youtu.be` |
| Errors mentioning `ffmpeg` / `ffprobe` | Install FFmpeg (see Setup step 4) and reopen the terminal |
| Download fails or "Sign in to confirm" errors | Update yt-dlp: `python -m pip install -U yt-dlp` |
