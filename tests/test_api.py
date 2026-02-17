from pathlib import Path

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from app.main import app
from app.subtitles import Segment
from app.transcriber import TranscriptionResult


client = TestClient(app)


def test_api_generates_translation_and_embedded_video(monkeypatch):
    def fake_transcribe_audio(file_path: Path, model_size: str, translate_to_english: bool):
        assert model_size == "small"
        assert translate_to_english is True
        return TranscriptionResult(
            full_text="Hello world",
            segments=[Segment(start=0.0, end=1.0, text="Hello world")],
        )

    def fake_burn_subtitles(input_video: Path, srt_file: Path, output_video: Path):
        assert srt_file.exists()
        output_video.write_bytes(b"fake-video")

    monkeypatch.setattr("app.main.transcribe_audio", fake_transcribe_audio)
    monkeypatch.setattr("app.main.burn_subtitles", fake_burn_subtitles)

    response = client.post(
        "/api/subtitulos",
        files={"audio": ("clip.mp4", b"video-content", "video/mp4")},
        data={"model_size": "small", "translate": "true"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["modo"] == "traduccion"
    assert payload["texto"] == "Hello world"
    assert payload["video_subtitulado_base64"]


def test_api_audio_does_not_generate_embedded_video(monkeypatch):
    def fake_transcribe_audio(file_path: Path, model_size: str, translate_to_english: bool):
        return TranscriptionResult(
            full_text="Hola",
            segments=[Segment(start=0.0, end=1.0, text="Hola")],
        )

    monkeypatch.setattr("app.main.transcribe_audio", fake_transcribe_audio)

    response = client.post(
        "/api/subtitulos",
        files={"audio": ("audio.mp3", b"audio-content", "audio/mpeg")},
        data={"model_size": "tiny"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["modo"] == "transcripcion"
    assert payload["video_subtitulado_base64"] is None
