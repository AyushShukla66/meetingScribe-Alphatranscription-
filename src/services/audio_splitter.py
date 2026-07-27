from pathlib import Path
from pydub import AudioSegment
import os


TEMP_FOLDER = Path("temp")

TEMP_FOLDER.mkdir(
    exist_ok=True
)



def split_audio(
    file_path,
    chunk_minutes=10
):


    # Check file exists

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            file_path
        )


    print(
        "Loading audio file..."
    )


    audio = AudioSegment.from_wav(
        file_path
    )


    total_duration = len(audio)


    print(
        "Audio duration:",
        round(total_duration / 60000, 2),
        "minutes"
    )


    chunk_size = (
        chunk_minutes * 60 * 1000
    )


    chunks = []



    chunk_number = 1



    for start in range(
        0,
        total_duration,
        chunk_size
    ):


        end = start + chunk_size


        chunk = audio[start:end]



        chunk_name = (

            TEMP_FOLDER /

            f"meeting_chunk_{chunk_number}.wav"

        )



        chunk.export(

            chunk_name,

            format="wav"

        )



        chunks.append(
            str(chunk_name)
        )


        print(
            "Created:",
            chunk_name
        )


        chunk_number += 1



    print(
        "Total chunks created:",
        len(chunks)
    )


    return chunks