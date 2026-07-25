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
        "Uploading audio for exact Hinglish transcription..."
    )


    for attempt in range(3):

        try:

            with open(audio_file, "rb") as file:


                result = client.audio.transcriptions.create(

                    model="whisper-1",

                    file=file,

                    prompt="""
                    Transcribe the audio exactly as spoken.

                    Follow these rules strictly:

                    - Keep the same language style used by the speaker.
                    - Do not translate Hindi words into English.
                    - Do not translate English words into Hindi.
                    - Do not convert Roman Hindi into Devanagari Hindi.
                    - Keep Hindi words in Roman Hindi.
                    - Keep English words exactly as English.
                    - Keep technical words unchanged.
                    - Keep API, software names, company names,
                      product names, and English terms unchanged.
                    - Do not summarize.
                    - Do not improve grammar.
                    - Do not rewrite sentences.
                    - Do not remove any words.

                    Example:

                    Spoken:
                    "Aaj meeting ke andar hum API integration discuss karenge
                    aur deployment ka flow dekhenge."

                    Correct transcript:
                    "Aaj meeting ke andar hum API integration discuss karenge
                    aur deployment ka flow dekhenge."

                    """
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