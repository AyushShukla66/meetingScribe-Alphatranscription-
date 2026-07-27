from models.meeting import SpeakerSegment



def format_time(seconds):

    minutes = int(seconds // 60)

    seconds = int(seconds % 60)

    return f"{minutes:02d}:{seconds:02d}"



def build_speaker_transcript(segments):

    transcript = ""


    for segment in segments:

        start = format_time(
            segment.start_time
        )


        transcript += (
            f"[00:{start}] "
            f"{segment.speaker}:\n"
        )


        transcript += (
            segment.text +
            "\n\n"
        )


    return transcript