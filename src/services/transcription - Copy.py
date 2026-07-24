from openai import OpenAI
from config.settings import OPENAI_API_KEY
from pathlib import Path
from pydub import AudioSegment

client = OpenAI(api_key=OPENAI_API_KEY)


def compress_audio(input_file):

    output_file = "temp/compressed.mp3"

    audio = AudioSegment.from_wav(input_file)

    audio.export(
        output_file,
        format="mp3",
        bitrate="64k"
    )

    return output_file


def transcribe_audio(audio_file):

    compressed_file = compress_audio(audio_file)

    with open(compressed_file, "rb") as file:

        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=file,
            language="en"
        )

    return transcript.text