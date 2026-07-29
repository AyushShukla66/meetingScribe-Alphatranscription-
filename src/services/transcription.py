import os
import time
from pathlib import Path

from openai import OpenAI
from pydub import AudioSegment

from config.settings import OPENAI_API_KEY


client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=300.0
)


TEMP_FOLDER = Path("temp/transcription_chunks")

# 10 minutes per chunk
CHUNK_LENGTH_MS = 10 * 60 * 1000



TRANSCRIPTION_PROMPT = """
You are a RAW VERBATIM speech-to-text transcription engine.

Your only job is to convert the speaker voice into text exactly as spoken.

The speaker may speak:
- Hindi
- English
- Hinglish (Hindi + English mix)

IMPORTANT:

Return only the transcript.

The output must always be:
Roman Hindi + English mix.

Never use Hindi Devanagari script.


STRICT VERBATIM RULES:

- Write every spoken word.
- Do not remove words.
- Do not add words.
- Keep repeated words.
- Keep repeated sentences.
- Keep self corrections.
- Keep mistakes.
- Keep filler words.
- Keep slang.
- Keep incomplete sentences.


Do NOT:
- Summarize.
- Explain.
- Rewrite.
- Correct grammar.
- Improve sentences.
- Translate.
- Remove repetitions.


Hindi:
Convert Hindi script to Roman Hindi only.
Do not translate Hindi meaning.

English:
Keep English words unchanged.

Hinglish:
Keep the natural Hindi + English order.


Keep unchanged:
- Software names
- API names
- Company names
- Product names
- Technical terms


Return ONLY the transcript.
"""



def split_audio(audio_file):
    """
    Split long audio into smaller chunks.
    """


    TEMP_FOLDER.mkdir(
        exist_ok=True
    )


    audio = AudioSegment.from_file(
        audio_file
    )


    chunks = []


    total_length = len(audio)


    start = 0

    index = 1


    while start < total_length:


        end = min(
            start + CHUNK_LENGTH_MS,
            total_length
        )


        chunk = audio[start:end]


        chunk_file = (
            TEMP_FOLDER /
            f"chunk_{index}.wav"
        )


        chunk.export(
            chunk_file,
            format="wav"
        )


        chunks.append(
            str(chunk_file)
        )


        print(
            f"Created chunk {index}:",
            round((end-start)/1000, 2),
            "seconds"
        )


        start = end

        index += 1



    return chunks





def transcribe_chunk(audio_file):
    """
    Transcribe one audio chunk.
    """


    for attempt in range(3):

        try:

            print(
                "Uploading:",
                audio_file
            )


            with open(
                audio_file,
                "rb"
            ) as file:


                result = client.audio.transcriptions.create(

                    model="gpt-4o-transcribe",

                    file=file,

                    prompt=TRANSCRIPTION_PROMPT

                )



            text = result.text.strip()



            if len(text) == 0:

                raise Exception(
                    "Empty transcript returned."
                )



            print(
                "Chunk completed."
            )


            return text



        except Exception as error:


            print(
                f"Chunk failed attempt {attempt + 1}"
            )


            print(error)


            time.sleep(5)



    raise Exception(
        f"Failed transcription for {audio_file}"
    )







def cleanup_chunks():

    """
    Delete temporary chunks.
    """


    if TEMP_FOLDER.exists():

        for file in TEMP_FOLDER.iterdir():

            file.unlink()






def transcribe_audio(audio_file):
    """
    Generate complete verbatim transcript.
    """


    if not os.path.exists(audio_file):

        raise FileNotFoundError(
            audio_file
        )



    print(
        "\nPreparing audio..."
    )



    try:


        chunks = split_audio(
            audio_file
        )


        print(
            f"Total chunks created: {len(chunks)}"
        )



        full_transcript = []



        for number, chunk in enumerate(chunks, start=1):


            print(
                f"\nTranscribing chunk {number}/{len(chunks)}"
            )


            text = transcribe_chunk(
                chunk
            )


            full_transcript.append(
                text
            )



        final_transcript = "\n".join(
            full_transcript
        )



        print(
            "\nComplete transcription finished."
        )


        print(
            "Transcript length:",
            len(final_transcript),
            "characters"
        )



        return final_transcript



    finally:


        cleanup_chunks()