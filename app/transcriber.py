from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import List

import whisper

from app.subtitles import Segment


@dataclass(slots=True)
class TranscriptionResult:
    full_text: str
    segments: List[Segment]


@lru_cache(maxsize=4)
def _load_model(model_size: str):
    return whisper.load_model(model_size)


def transcribe_spanish(file_path: Path, model_size: str = "small") -> TranscriptionResult:
    model = _load_model(model_size)
    result = model.transcribe(
        str(file_path),
        language="es",
        task="transcribe",
        temperature=0,
        fp16=False,
        verbose=False,
    )

    segments = [
        Segment(start=float(item["start"]), end=float(item["end"]), text=str(item["text"]))
        for item in result.get("segments", [])
    ]

    return TranscriptionResult(
        full_text=str(result.get("text", "")).strip(),
        segments=segments,
    )
