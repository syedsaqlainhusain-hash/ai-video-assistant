import whisper
import os

# Whisper calls ffmpeg itself, so make sure it can find it
FFMPEG_DIR = r"C:\Users\HP\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin"
os.environ["PATH"] += os.pathsep + FFMPEG_DIR

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

_model = None


def load_model():
    """Load the Whisper model based on the specified model size."""
    global _model
    if _model is None:
        print(f"Loading Whisper model: {WHISPER_MODEL}")
        _model = whisper.load_model(WHISPER_MODEL)
        print("Model loaded successfully.")

    return _model


def transcribe_chunk(chunk_path: str, translate: bool = False) -> str:
    """Transcribe a single audio chunk using the Whisper model."""
    model = load_model()
    task = "translate" if translate else "transcribe"
    result = model.transcribe(chunk_path, task=task, fp16=False)
    return result["text"]


def transcribe_all(chunks: list, translate: bool = False) -> str:
    full_transcript = ""

    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i + 1}/{len(chunks)}")
        text = transcribe_chunk(chunk, translate=translate)
        full_transcript += text + " "

    print("Transcription completed.")
    return full_transcript