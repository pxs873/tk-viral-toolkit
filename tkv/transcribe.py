"""Transcription module - wraps faster-whisper for audio transcription."""

import subprocess
import json
from pathlib import Path


def extract_audio(video_path: str | Path, out_path: str | Path | None = None) -> Path:
    """Extract audio track from video via ffmpeg."""
    video_path = Path(video_path)
    out_path = Path(out_path) if out_path else video_path.with_suffix(".wav")
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(video_path), "-vn",
         "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", str(out_path)],
        capture_output=True, check=True,
    )
    return out_path


def transcribe(audio_path: str | Path, model: str = "small",
               language: str | None = None) -> list[dict]:
    """Transcribe audio with faster-whisper.

    Returns list of segments: [{"start": float, "end": float, "text": str}]
    """
    try:
        from faster_whisper import FasterWhisperModel
    except ImportError:
        raise RuntimeError("pip install faster-whisper to use transcription")

    fw = FasterWhisperModel(model, device="cpu", compute_type="int8")
    segments, _ = fw.transcribe(str(audio_path), language=language,
                                vad_filter=True)
    return [
        {"start": round(s.start, 2), "end": round(s.end, 2),
         "text": s.text.strip()}
        for s in segments
    ]


def transcribe_to_file(video_path: str | Path, out_json: str | Path | None = None,
                       model: str = "small") -> Path:
    """Full pipeline: video -> audio -> transcript JSON."""
    video_path = Path(video_path)
    audio = extract_audio(video_path)
    segments = transcribe(audio, model=model)
    out_json = Path(out_json) if out_json else video_path.with_suffix(".transcript.json")
    out_json.write_text(json.dumps(segments, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    return out_json
