import ollama
import json
import datetime
import math
import random
import re

MODEL_NAME = "llama3:latest"

# =========================
# TOOLS
# =========================

def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%A, %d %b %Y | %I:%M %p")


def calculate(expression):
    try:
        safe_names = {
            k: v
            for k, v in math.__dict__.items()
            if not k.startswith("_")
        }

        result = eval(
            expression,
            {"__builtins__": {}},
            safe_names
        )

        return f"Answer: {round(result, 6)}"

    except Exception as e:
        return f"Math Error: {str(e)}"


def word_count(text):
    words = len(text.split())
    chars = len(text)
    chars_no_space = len(text.replace(" ", ""))

    return (
        f"Words: {words} | "
        f"Characters: {chars} | "
        f"Characters(No Spaces): {chars_no_space}"
    )


def generate_quiz(topic, num_questions=1):

    questions = {
        "python": [
            {
                "question": "What does len() do?",
                "options": [
                    "Count items",
                    "Delete items",
                    "Sort items",
                    "Print items"
                ],
                "answer": "Count items"
            },
            {
                "question": "Which datatype is immutable?",
                "options": [
                    "List",
                    "Tuple",
                    "Dictionary",
                    "Set"
                ],
                "answer": "Tuple"
            }
        ],

        "ai": [
            {
                "question": "What does LLM stand for?",
                "options": [
                    "Large Language Model",
                    "Long Logic Machine",
                    "Linear Learning Machine",
                    "Language Logic Memory"
                ],
                "answer": "Large Language Model"
            },
            {
                "question": "What is overfitting?",
                "options": [
                    "Learning too much training data",
                    "GPU failure",
                    "Database issue",
                    "Memory leak"
                ],
                "answer": "Learning too much training data"
            }
        ]
    }

    topic = topic.lower()

    if "python" in topic:
        selected = questions["python"]
    else:
        selected = questions["ai"]

    random.shuffle(selected)
    selected = selected[:num_questions]

    output = ""

    for i, q in enumerate(selected, start=1):

        output += f"\nQ{i}. {q['question']}\n"

        for idx, opt in enumerate(q["options"], start=1):
            output += f"  {idx}. {opt}\n"

        output += f"Answer: {q['answer']}\n"

    return output


# =========================
# TOOL REGISTRY
# =========================

TOOLS = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "word_count": word_count,
    "generate_quiz": generate_quiz
}


# =========================
# SYSTEM PROMPT
# =========================

SYSTEM_PROMPT = """
You are SmartBuddy AI.

You can:
- Answer questions
- Solve math
- Tell time
- Count words
- Generate quizzes
- Explain concepts

IMPORTANT:

If a tool is required, respond ONLY in JSON.

FORMAT:
{"tool":"tool_name","args":{"key":"value"}}

EXAMPLES:

{"tool":"get_current_time","args":{}}

{"tool":"calculate","args":{"expression":"5*8"}}

{"tool":"word_count","args":{"text":"hello world"}}

DO NOT:
- Explain before JSON
- Use markdown
- Use code blocks
"""


chat_history = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

question_count = 0


# =========================
# START SCREEN
# =========================

print("=" * 65)
print("        SMARTBUDDY AI - FINAL MINI PROJECT")
print("=" * 65)

print(f"Model Loaded: {MODEL_NAME}")

print("\nFeatures:")
print("✓ Tool Calling")
print("✓ Conversational Memory")
print("✓ Quiz Generator")
print("✓ Math Solver")
print("✓ Structured JSON Outputs")

print("\nExamples:")
print("- what time is it")
print("- calculate sqrt(144)")
print("- count words in hello world")
print("- give 2 ai quiz questions")

print("\nType 'exit' to quit\n")


# =========================
# MAIN LOOP
# =========================

while True:

    user_input = input("You: ").strip()

    if user_input.lower() == "exit":

        print("\nSmartBuddy: Goodbye!")

        print(
            f"Questions Answered: {question_count}"
        )

        break

    if not user_input:
        continue

    question_count += 1

    chat_history.append({
        "role": "user",
        "content": user_input
    })

    print("\nSmartBuddy is thinking...\n")

    response = ollama.chat(
        model=MODEL_NAME,
        messages=chat_history,
        options={
            "temperature": 0,
            "top_p": 0.1
        }
    )

    raw = response["message"]["content"].strip()

    print("[RAW OUTPUT]")
    print(raw)

    tool_used = False

    if raw.startswith("{"):

        try:

            call = json.loads(raw)

            tool_name = call.get("tool")
            args = call.get("args", {})

            if tool_name in TOOLS:

                print(f"\n[USING TOOL: {tool_name}]")

                tool_result = TOOLS[tool_name](**args)

                print("\n[TOOL RESULT]")
                print(tool_result)

                chat_history.append({
                    "role": "assistant",
                    "content": raw
                })

                chat_history.append({
                    "role": "user",
                    "content": (
                        f"Tool Result: {tool_result}. "
                        f"Now answer naturally."
                    )
                })

                final_response = ollama.chat(
                    model=MODEL_NAME,
                    messages=chat_history,
                    options={
                        "temperature": 0,
                        "top_p": 0.1
                    }
                )

                final_reply = (
                    final_response["message"]["content"]
                )

                print(f"\nSmartBuddy: {final_reply}\n")

                chat_history.append({
                    "role": "assistant",
                    "content": final_reply
                })

                tool_used = True

        except Exception as e:

            print("\n[JSON ERROR]")
            print(str(e))

    if not tool_used:

        print(f"\nSmartBuddy: {raw}\n")

        chat_history.append({
            "role": "assistant",
            "content": raw
        })

    print(
        f"[Question #{question_count} | "
        f"Memory: {len(chat_history)} msgs]\n"
    )