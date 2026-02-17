import importlib
import sys
from pathlib import Path
from types import SimpleNamespace


class DummyModel:
    def __init__(self):
        self.last_kwargs = None

    def transcribe(self, *_args, **kwargs):
        self.last_kwargs = kwargs
        return {
            "text": " Hola mundo ",
            "segments": [
                {"start": 0, "end": 1.2, "text": " Hola"},
            ],
        }


def test_transcribe_spanish_forces_spanish_and_no_translation(monkeypatch):
    dummy_model = DummyModel()

    monkeypatch.setitem(sys.modules, "whisper", SimpleNamespace(load_model=lambda _: dummy_model))

    transcriber = importlib.import_module("app.transcriber")
    transcriber._load_model.cache_clear()

    result = transcriber.transcribe_spanish(Path("audio.mp3"), model_size="small")

    assert dummy_model.last_kwargs["language"] == "es"
    assert dummy_model.last_kwargs["task"] == "transcribe"
    assert dummy_model.last_kwargs["initial_prompt"] == "Transcribe el audio en español. No traduzcas."
    assert result.full_text == "Hola mundo"
    assert len(result.segments) == 1
