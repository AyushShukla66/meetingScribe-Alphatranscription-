from openai import OpenAI
from config.settings import OPENAI_API_KEY

import os
import time


client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=300.0
)



def transcribe_audio(audio_file):

    if not os.path.exists(audio_file):

        raise FileNotFoundError(
            audio_file
        )


    size_mb = (
        os.path.getsize(audio_file)
        /
        (1024 * 1024)
    )


    print(
        "Audio size:",
        round(size_mb, 2),
        "MB"
    )


    print(
        "Uploading audio for English transcription..."
    )


    for attempt in range(3):

        try:

            with open(audio_file, "rb") as file:

                result = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=file,
                )


            print(
                "Transcription completed"
            )


            return result.text


        except Exception as e:

            print(
                "Transcription attempt failed:",
                attempt + 1
            )

            print(e)

            time.sleep(5)


    raise Exception(
        "Transcription failed after retries"
    )