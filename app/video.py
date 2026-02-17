from __future__ import annotations

import subprocess
from pathlib import Path


def burn_subtitles(input_video: Path, srt_file: Path, output_video: Path) -> None:
    """Incrusta subtítulos SRT en el vídeo usando ffmpeg."""

    subtitle_path = str(srt_file).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_video),
        "-vf",
        f"subtitles='{subtitle_path}'",
        "-c:a",
        "copy",
        str(output_video),
    ]

    completed = subprocess.run(command, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "ffmpeg no pudo incrustar los subtítulos")
