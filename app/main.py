from __future__ import annotations

import tempfile
import base64
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from dataclasses import asdict

from app.subtitles import to_srt, to_vtt
from app.transcriber import transcribe_audio
from app.video import burn_subtitles

ALLOWED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".mp4",
    ".webm",
    ".ogg",
    ".flac",
    ".aac",
    ".mpeg",
}

VIDEO_EXTENSIONS = {".mp4", ".webm", ".mpeg"}

app = FastAPI(title="Generador de subtítulos en castellano")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/subtitulos")
async def generar_subtitulos(
    audio: UploadFile = File(...),
    model_size: str = Form("small"),
    translate: bool = Form(False),
):
    extension = Path(audio.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        return JSONResponse(
            status_code=400,
            content={"error": "Formato no soportado. Usa audio/video común (mp3, wav, mp4, webm...)."},
        )

    with tempfile.TemporaryDirectory(prefix="subtitulos-") as temp_dir:
        input_path = Path(temp_dir) / f"entrada{extension}"
        with input_path.open("wb") as f:
            f.write(await audio.read())

        try:
            result = transcribe_audio(
                input_path,
                model_size=model_size,
                translate_to_english=translate,
            )
        except Exception as exc:
            return JSONResponse(status_code=500, content={"error": f"Error al transcribir: {exc}"})

        srt_content = to_srt(result.segments)
        vtt_content = to_vtt(result.segments)

        subtitled_video_b64 = None
        if extension in VIDEO_EXTENSIONS:
            srt_path = Path(temp_dir) / "subtitulos.srt"
            output_video = Path(temp_dir) / f"subtitulado{extension}"
            srt_path.write_text(srt_content, encoding="utf-8")

            try:
                burn_subtitles(input_path, srt_path, output_video)
                subtitled_video_b64 = base64.b64encode(output_video.read_bytes()).decode("utf-8")
            except Exception:
                subtitled_video_b64 = None

        return {
            "texto": result.full_text,
            "srt": srt_content,
            "vtt": vtt_content,
            "segmentos": [asdict(segment) for segment in result.segments],
            "modo": "traduccion" if translate else "transcripcion",
            "video_subtitulado_base64": subtitled_video_b64,
        }
