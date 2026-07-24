from openai import OpenAI
from config.settings import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_executive_brief(transcript):

    prompt = f"""
You are an Executive Assistant.

From the meeting transcript below generate:

1. Executive Summary
2. Decisions
3. Action Items
4. Risks
5. Director Attention

Transcript:
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