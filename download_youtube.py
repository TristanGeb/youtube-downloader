#!/usr/bin/env python3
"""Download a YouTube video you own or are authorized to download.

Requires yt-dlp: python -m pip install yt-dlp
"""

import argparse
from pathlib import Path
from urllib.parse import urlparse

YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download a YouTube video that you own or are authorized to download."
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("."),
        help="directory for the download (default: current directory)",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=("mp4", "mp3", "both"),
        default="mp4",
        help="download as mp4 video, mp3 audio, or both (default: mp4)",
    )
    parser.add_argument(
        "-p",
        "--playlist",
        action="store_true",
        help="download every video in the playlist instead of a single video",
    )
    args = parser.parse_args()

    parsed_url = urlparse(args.url)
    if parsed_url.scheme not in {"http", "https"} or parsed_url.hostname not in YOUTUBE_HOSTS:
        parser.error("please provide a valid YouTube URL")

    args.output.mkdir(parents=True, exist_ok=True)
    options = {
        "outtmpl": str(args.output / "%(title)s.%(ext)s"),
        "noplaylist": not args.playlist,
    }
    if args.playlist:
        # Skip private/deleted videos instead of stopping the whole run.
        options["ignoreerrors"] = True
        # Remember finished videos so an interrupted run resumes where it left off.
        options["download_archive"] = str(args.output / "_archive.txt")
    if args.format == "mp3":
        options["format"] = "bestaudio/best"
        options["postprocessors"] = [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}
        ]
    else:
        options["format"] = "bestvideo*+bestaudio/best"
        options["merge_output_format"] = "mp4"
        if args.format == "both":
            options["keepvideo"] = True
            options["postprocessors"] = [
                {"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}
            ]

    try:
        import yt_dlp
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency: yt-dlp. Install it with: python -m pip install yt-dlp"
        ) from exc

    with yt_dlp.YoutubeDL(options) as downloader:
        downloader.download([args.url])


if __name__ == "__main__":
    main()
