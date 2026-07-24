from pathlib import Path
from docx import Document

from services.transcription import transcribe_audio


def generate_report(meeting):

    # Create reports folder
    Path("reports").mkdir(exist_ok=True)


    # Get transcript
    transcript = transcribe_audio(
        "temp/meeting.wav"
    )


    print("======== TRANSCRIPT ========")
    print(transcript)
    print("============================")


    # Create Word file
    doc = Document()


    doc.add_heading(
        "Finodaya Capital",
        level=1
    )

    doc.add_heading(
        "Meeting Transcript",
        level=2
    )


    doc.add_paragraph(
        f"Meeting Name: {meeting.name}"
    )


    doc.add_paragraph(
        f"Start Time: {meeting.start_time}"
    )


    doc.add_paragraph(
        f"End Time: {meeting.end_time}"
    )


    doc.add_heading(
        "Transcript",
        level=2
    )


    # Add exact speech text
    doc.add_paragraph(
        transcript
    )


    # Save file
    filename = (
        f"reports/{meeting.name}.docx"
    )


    doc.save(filename)


    print(
        "DOCX FILE CREATED:",
        Path(filename).absolute()
    )


    return filename