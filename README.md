# Video Subtítulos (reescrito)

Aplicación web para **transcribir/traducir audio-vídeo y generar subtítulos** usando Whisper local.

## Qué hace

- Sube un archivo de audio o vídeo (`mp3`, `wav`, `m4a`, `mp4`, `webm`, etc.).
- Fuerza el idioma de entrada en español (`language="es"`) para mejorar resultados en castellano.
- Permite traducir al inglés usando Whisper (`task="translate"`).
- Devuelve:
  - Transcripción completa.
  - Subtítulos en formato **SRT**.
  - Subtítulos en formato **VTT**.
  - Vídeo con subtítulos incrustados (si subes un archivo de vídeo).

## Requisitos

- Python 3.10+
- `ffmpeg` instalado en el sistema (necesario para Whisper con varios formatos)

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Abrir en navegador: `http://localhost:8000`

## Tests

```bash
pytest -q
```

## Estructura

- `app/main.py`: API y servidor web.
- `app/transcriber.py`: integración con Whisper para transcripción/traducción.
- `app/subtitles.py`: conversión de segmentos a SRT/VTT.
- `app/video.py`: incrustación de subtítulos en vídeo con ffmpeg.
- `templates/index.html`: interfaz web.
- `static/style.css`: estilos.
