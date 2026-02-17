from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(slots=True)
class Segment:
    """Representa un segmento de subtítulo con tiempos en segundos."""

    start: float
    end: float
    text: str


def _format_timestamp(seconds: float, decimal_separator: str = ",") -> str:
    if seconds < 0:
        seconds = 0.0
    millis = int(round(seconds * 1000))
    hours = millis // 3_600_000
    millis -= hours * 3_600_000
    minutes = millis // 60_000
    millis -= minutes * 60_000
    secs = millis // 1_000
    millis -= secs * 1_000
    return f"{hours:02}:{minutes:02}:{secs:02}{decimal_separator}{millis:03}"


def to_srt(segments: Iterable[Segment]) -> str:
    blocks: List[str] = []
    for index, segment in enumerate(segments, start=1):
        text = segment.text.strip()
        if not text:
            continue
        start = _format_timestamp(segment.start, decimal_separator=",")
        end = _format_timestamp(segment.end, decimal_separator=",")
        blocks.append(f"{index}\n{start} --> {end}\n{text}\n")
    return "\n".join(blocks).strip() + "\n"


def to_vtt(segments: Iterable[Segment]) -> str:
    blocks: List[str] = ["WEBVTT\n"]
    for segment in segments:
        text = segment.text.strip()
        if not text:
            continue
        start = _format_timestamp(segment.start, decimal_separator=".")
        end = _format_timestamp(segment.end, decimal_separator=".")
        blocks.append(f"{start} --> {end}\n{text}\n")
    return "\n".join(blocks).strip() + "\n"
