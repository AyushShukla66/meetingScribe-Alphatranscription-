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
        raise FileNotFoundError(audio_file)


    size_mb = os.path.getsize(audio_file) / (1024 * 1024)


    print(
        "Audio size:",
        round(size_mb, 2),
        "MB"
    )


    print(
        "Uploading audio for transcription..."
    )


    for attempt in range(3):

        try:

            with open(audio_file, "rb") as file:


                result = client.audio.transcriptions.create(

                    model="gpt-4o-transcribe",

                    file=file,


                    prompt="""

This is a professional business meeting recording.

Transcribe the audio accurately.

Important rules:

- Preserve Hindi, English, and Hinglish exactly.
- Do not translate languages.
- Do not summarize.
- Do not rewrite sentences.
- Do not add extra information.
- Remove obvious Whisper mistakes.
- Keep technical terms unchanged.

Keep these words exactly if spoken:

API
Backend
Frontend
Deployment
Database
Server
Authentication
OpenAI
Python
Software names
Company names
Product names


The output should be a clean readable transcript.

Example:

Audio:
"humko is tool ke baare mein discuss karna hai ki organization mein deploy karna hai ya nahi"

Output:
"humko is tool ke baare mein discuss karna hai ki organization mein deploy karna hai ya nahi"

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
        "Transcription failed after retries."
    )