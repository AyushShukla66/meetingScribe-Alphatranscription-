from pathlib import Path
from docx import Document

from openai import OpenAI
from config.settings import OPENAI_API_KEY

from services.transcription import transcribe_audio
from services.transcript_cleaner import clean_transcript


client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=300.0
)



def generate_report(meeting):


    # Create reports folder
    Path("reports").mkdir(
        exist_ok=True
    )



    print(
        "Generating transcript..."
    )


    # Step 1:
    # Get Hinglish transcript from audio

    raw_transcript = transcribe_audio(
        "temp/meeting.wav"
    )


    print(
        "======== RAW TRANSCRIPT ========"
    )

    print(raw_transcript)

    print(
        "================================"
    )



    print(
        "Cleaning transcript..."
    )


    # Step 2:
    # Clean Hinglish transcript
    # No translation

    transcript = clean_transcript(
        raw_transcript
    )


    print(
        "======== CLEAN TRANSCRIPT ========"
    )

    print(transcript)

    print(
        "=================================="
    )



    print(
        "Generating meeting summary..."
    )



    # Step 3:
    # Generate English meeting report

    report_response = client.chat.completions.create(


        model="gpt-4o-mini",


        messages=[


            {

                "role": "system",

                "content": """

You are a professional corporate meeting report generator.

Create a structured meeting report from the Hinglish transcript.

Generate only:

1. Meeting Topic

2. Key Discussion Points

3. Decisions Made

4. Action Items


Rules:

- Write the report in professional English.
- Do not include the transcript.
- Do not translate the transcript section.
- Only summarize the meeting content.
- Do not add information that was not discussed.
- Keep technical terms unchanged.
- Keep API names, software names, company names, and product names unchanged.

"""

            },


            {

                "role": "user",

                "content": transcript

            }

        ]

    )



    meeting_report = (
        report_response
        .choices[0]
        .message
        .content
    )



    # Step 4:
    # Create DOCX file


    doc = Document()



    doc.add_heading(
        "Finodaya Capital",
        level=1
    )



    doc.add_heading(
        "Meeting Report",
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



    # English Summary

    doc.add_heading(
        "Summary",
        level=2
    )


    doc.add_paragraph(
        meeting_report
    )



    # Hinglish Transcript

    doc.add_heading(
        "Meeting Transcript",
        level=2
    )


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