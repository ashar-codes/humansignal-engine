import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


SYSTEM_PROMPT = """
You are a psychological signal extraction engine.

Analyze the conversation and detect:

1. Emotional signals:
   - validation
   - dismissal
   - guilt induction
   - blame shifting
   - repair attempt
   - escalation

2. Behavioral signals:
   - dominance behavior
   - manipulation
   - emotional withdrawal
   - emotional dependency

3. Attachment indicators:
   - secure
   - anxious
   - avoidant

Return structured JSON only in this format:

{
  "emotional_signals": [
      {"speaker": "A", "type": "", "intensity": 1}
  ],
  "behavioral_signals": [
      {"speaker": "A", "category": "", "weight": 1}
  ],
  "attachment_a": "",
  "attachment_b": ""
}
"""


def extract_signals(conversation_text: str):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": conversation_text}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

