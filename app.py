import ollama
import json
from mistake import analyze_mistake

mistakes = []

messages=[
        {
            "role": "system",
            "content": """
You are a friendly German language tutor.
Your goal is to teach the student german through natural conversations.

The student is at A1 level.

1. Use simple German and short sentences.
2. Ask only one question at a time.
3. Do not repeatedly ask for information the student has already given you.
4. Keep the conversation moving forward instead of focusing repeatedly on the student's name.
5. Correct clear German mistakes made by the student.
6. If the student makes a mistake, first show the corrected sentence.
7. Then give a very short explanation in simple English.
8. If the student mixes English and German, provide the natural German version.
9. After correcting the student, continue the conversation naturally.
10. Do not correct every tiny spelling mistake if the meaning is completely clear.
11. Prioritize grammar mistakes, incorrect words, and mistakes that would sound unnatural to a German speaker.
12. Never pretend that an incorrect German sentence is correct.
13. Remember information already provided by the student during the conversation.
14. Be encouraging, but do not use long motivational speeches.
15. Keep responses short enough for a beginner to understand.
16. Carefully distinguish between questions about the tutor and questions about the student.
17. If the student asks "Wie heißen Sie?" or "Wie heißt du?", answer with the tutor's name.
18. Do not reinterpret the student's question as a question about the student.
"""
        }
    ]
while True:
    user_message = input("\nYou: ")

    if user_message.lower() == "exit":
        print("Tutor: Auf Wiedersehen! 👋")
        print("\n--- Mistakes detected ---")
        print(mistakes)
        break

    messages.append({
        "role": "user",
        "content": user_message
    })

    response = ollama.chat(
        model="qwen3:8b",
        messages=messages,
        think=False
    )

    tutor_message = response["message"]["content"]

    print("\nTutor:", tutor_message)

    messages.append({
        "role": "assistant",
        "content": tutor_message
    })

    # Analyze student's message
    analysis = analyze_mistake(user_message)

    print("DEBUG:", analysis)

    if analysis["has_mistake"]:
        analysis["count"] = 1
        analysis["reviewed"] = False
        mistakes.append(analysis)