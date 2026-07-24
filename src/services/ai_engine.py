from openai import OpenAI
from config.settings import OPENAI_API_KEY


client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=300.0
)



def generate_executive_brief(transcript):

    prompt = f"""
You are an Executive Assistant.

Generate the report in English only.

Do not change the transcript.
Do not translate the transcript.
Do not summarize the transcript.

Create:

1. Executive Summary
2. Decisions
3. Action Items
4. Risks
5. Director Attention

Use this transcript:

{transcript}
"""


    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response.choices[0].message.content