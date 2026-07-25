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

Generate a clean Hinglish transcript.

Important rules:

- Do NOT translate Hindi into English.
- Do NOT translate English into Hindi.
- Keep Hindi sentences in Roman Hindi.
- Keep English words as English.
- Maintain the natural Hinglish speaking style.

Examples:

Audio:
"humko is tool ke baare mein discuss karna hai ki humko isko organization mein deploy karna hai ya nahi"

Correct output:
"humko is tool ke baare mein discuss karna hai ki humko isko organization mein deploy karna hai ya nahi"


Audio:
"aaj hum API integration aur backend deployment ke baare mein baat karenge"

Correct output:
"aaj hum API integration aur backend deployment ke baare mein baat karenge"


Rules:
- Do not summarize.
- Do not rewrite.
- Do not improve grammar.
- Do not convert into formal English.
- Remove only completely wrong speech recognition errors.
- Keep company names, software names and technical words unchanged.

Return only transcript.

"""

                )


            print(
                "Transcription completed"
            )


            return result.text



        except Exception as e:


            print(
                "Transcription failed attempt:",
                attempt + 1
            )


            print(e)


            time.sleep(5)



    raise Exception(
        "Transcription failed after retries."
    )