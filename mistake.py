import ollama
import json


def analyze_mistake(student_message):

    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "system",
                "content": """
You are a German grammar analyzer.

Analyze the student's message.

Return ONLY valid JSON:

{
    "has_mistake": true or false,
    "mistake": "the incorrect part",
    "correction": "the corrected version",
    "topic": "the grammar or vocabulary topic"
}

Rules:
- If the student's German is correct, return has_mistake as false.
- Do not invent mistakes.
- Ignore minor spelling mistakes when the meaning is completely clear.
- If the message is in English, do not treat it as a German mistake.
- Do not explain anything outside the JSON.
"""
            },
            {
                "role": "user",
                "content": student_message
            }
        ],
        think=False
    )

    result = response["message"]["content"]

    return json.loads(result)

if __name__ == "__main__":
    test = "I went to the supermarket yesterday."

    result = analyze_mistake(test)

    print(result)