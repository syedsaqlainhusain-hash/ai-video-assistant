from utils.audio_processor import process_input
from core.transcriber import transcribe_all

if __name__ == "__main__":
    source = "https://youtu.be/mtiOK2QG9Q0?si=d43V6V9esWrD42cZ"

    chunks = process_input(source)
    transcript = transcribe_all(chunks)

    print("\n--- TRANSCRIPT ---\n")
    print(transcript)

    with open("transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript)