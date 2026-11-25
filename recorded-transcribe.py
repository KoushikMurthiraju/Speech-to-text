import whisper

def transcribe_audio(audio_path: str, model_name: str = "base") -> str:
    """
    Transcribes an audio file using OpenAI Whisper.

    :param audio_path: path to the audio file (.mp3, .wav, .m4a, etc.)
    :param model_name: tiny | base | small | medium | large
    :return: transcribed text
    """
    print(f"Loading model '{model_name}' (first time may be slow)...")
    model = whisper.load_model(model_name)

    print(f"Transcribing: {audio_path}")
    result = model.transcribe(audio_path)

    text = result["text"].strip()
    return text


if __name__ == "__main__":
    # 🔁 1. CHANGE THIS PATH TO YOUR AUDIO FILE
    audio_file = "Rev.mp3"   # e.g. "recording.wav"

    transcript = transcribe_audio(audio_file, model_name="base")

    print("\n--- TRANSCRIPT ---\n")
    print(transcript)

    # 💾 Optional: save to file
    with open("transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript)

    print("\nTranscript saved to transcript.txt ✅")
