"""CLI entry point: tkv download/transcribe/analyze."""

import argparse
import json
import sys
from pathlib import Path

from .download import download, extract_video_id
from .transcribe import transcribe_to_file
from .analyze import new_breakdown, save_breakdown, render_markdown


def cmd_process(args):
    """Full pipeline: download -> transcribe -> scaffold breakdown."""
    url = args.url
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[1/3] Downloading {url} ...")
    video = download(url, out_dir, proxy=args.proxy)
    if not video:
        sys.exit("Download failed.")
    print(f"      -> {video}")

    transcript = []
    if not args.skip_transcribe:
        print("[2/3] Transcribing ...")
        tpath = transcribe_to_file(video, model=args.whisper_model)
        transcript = json.loads(tpath.read_text(encoding="utf-8"))
        print(f"      -> {tpath} ({len(transcript)} segments)")

    print("[3/3] Creating breakdown scaffold ...")
    video_id = extract_video_id(url) or video.stem
    bd = new_breakdown(video_id, args.author or "unknown", video, transcript)
    bpath = save_breakdown(bd, out_dir / f"{video_id}.breakdown.json")
    mpath = out_dir / f"{video_id}.breakdown.md"
    mpath.write_text(render_markdown(bd), encoding="utf-8")
    print(f"      -> {bpath}")
    print(f"      -> {mpath}")
    print("Done. Fill in the 4 layers + 5 pieces in the Markdown file.")


def main():
    p = argparse.ArgumentParser(
        prog="tkv",
        description="TikTok viral video breakdown toolkit: download + transcribe + analyze",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    pp = sub.add_parser("process", help="full pipeline for one video URL")
    pp.add_argument("url", help="tiktok.com/@user/video/xxx URL")
    pp.add_argument("-o", "--out", default="./output", help="output directory")
    pp.add_argument("--author", default="", help="video author @handle")
    pp.add_argument("--proxy", default=None, help="HTTP proxy URL for yt-dlp")
    pp.add_argument("--whisper-model", default="small",
                    choices=["tiny", "base", "small", "medium"],
                    help="faster-whisper model size")
    pp.add_argument("--skip-transcribe", action="store_true",
                    help="skip transcription step")
    pp.set_defaults(func=cmd_process)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
