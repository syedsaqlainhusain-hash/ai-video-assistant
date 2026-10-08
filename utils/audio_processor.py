import yt_dlp
import os
from pydub import AudioSegment

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

FFMPEG_DIR = r"C:\Users\HP\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin"

# Tell pydub where ffmpeg/ffprobe are
AudioSegment.converter = os.path.join(FFMPEG_DIR, "ffmpeg.exe")
AudioSegment.ffprobe = os.path.join(FFMPEG_DIR, "ffprobe.exe")


def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "cookiesfrombrowser": ("firefox",),
        "ffmpeg_location": FFMPEG_DIR,
        "remote_components": ["ejs:github"],
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "wav"}
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return os.path.splitext(filename)[0] + ".wav"


def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")
    return output_path


def chunk_audio(wav_path: str, chunk_length: int = 10) -> list:
    """Chunk a WAV audio file into smaller segments of specified length in seconds."""
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_length * 1000
    base = os.path.splitext(wav_path)[0]
    chunks = []
    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start:start + chunk_ms]
        chunk_path = f"{base}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
    return chunks


def process_input(sources: str) -> list:
    """Process the input source, which can be a YouTube URL or a local file path."""
    if sources.startswith("http"):
        print("detected youtube url, downloading audio...")
        downloaded = download_youtube_audio(sources)
        wav_path = convert_to_wav(downloaded)
    else:
        print("detected local file, converting to wav...")
        wav_path = convert_to_wav(sources)

    print("chunking audio...")
    chunks = chunk_audio(wav_path, chunk_length=30)
    print(f"audio ready - {len(chunks)} chunks created")
    return chunks


if __name__ == "__main__":
    url = "https://youtu.be/mtiOK2QG9Q0?si=d43V6V9esWrD42cZ"
    print(process_input(url))