import ollama
import json
import datetime
import math
import random
import re

# ==============================================================================
# SELECT MODEL
# ==============================================================================

MODEL_NAME = "llama3:latest"

# ==============================================================================
# TOOL DEFINITIONS
# ==============================================================================

def get_current_time():
    """Returns current date and time."""
    now = datetime.datetime.now()
    return now.strftime(
        "Date: %A, %d %B %Y | Time: %I:%M %p"
    )


def calculate(expression):
    """Safely evaluates math expressions."""
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

        return (
            f"Result of '{expression}' = "
            f"{round(result, 6)}"
        )

    except Exception as e:
        return f"Math error: {str(e)}"


def word_count(text):
    """Counts words, characters and sentences."""

    words = len(text.split())
    chars = len(text)

    chars_no_space = len(
        text.replace(" ", "")
    )

    sentences = (
        text.count(".")
        + text.count("!")
        + text.count("?")
    )

    return (
        f"Words: {words} | "
        f"Characters: {chars} | "
        f"Characters (no spaces): {chars_no_space} | "
        f"Sentences: {sentences}"
    )


def generate_quiz(topic):
    """Generates quiz questions."""

    questions = {
        "python": [
            "What does len() do in Python?",
            "What is the difference between a list and tuple?",
            "What is a dictionary in Python?",
            "What does import do in Python?"
        ],
        "ai": [
            "What is supervised learning?",
            "What does LLM stand for?",
            "What is overfitting?",
            "What is a neural network?"
        ],
        "general": [
            "What is RAM?",
            "What does CPU stand for?",
            "What is an API?",
            "What is open-source software?"
        ]
    }

    topic_lower = topic.lower()

    if "python" in topic_lower:
        q = random.choice(questions["python"])

    elif "ai" in topic_lower or "ml" in topic_lower:
        q = random.choice(questions["ai"])

    else:
        q = random.choice(questions["general"])

    return f"Quiz question on '{topic}': {q}"


# ==============================================================================
# TOOL REGISTRY
# ==============================================================================

TOOLS = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "word_count": word_count,
    "generate_quiz": generate_quiz
}

# ==============================================================================
# SYSTEM PROMPT
# ==============================================================================

SYSTEM_PROMPT = """
You are an AI assistant with access to tools.

AVAILABLE TOOLS:

1. get_current_time()
   - returns current date and time

2. calculate(expression)
   - solves mathematical expressions

3. word_count(text)
   - counts words and characters

4. generate_quiz(topic)
   - generates quiz questions

IMPORTANT RULES:

- If a tool is needed, respond ONLY with JSON.
- Never explain before JSON.
- Never use markdown.
- Never use code blocks.
- JSON must always be valid.

FORMAT:

{"tool":"tool_name","args":{"arg":"value"}}

EXAMPLES:

User: what time is it?
Assistant:
{"tool":"get_current_time","args":{}}

User: calculate 25*8
Assistant:
{"tool":"calculate","args":{"expression":"25*8"}}

User: count words in 'Hello world!'
Assistant:
{"tool":"word_count","args":{"text":"Hello world!"}}

User: give me a quiz on Python
Assistant:
{"tool":"generate_quiz","args":{"topic":"Python"}}

After tool result is provided,
respond naturally and helpfully.
"""

# ==============================================================================
# CHAT HISTORY
# ==============================================================================

chat_history = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

# ==============================================================================
# START SCREEN
# ==============================================================================

print("=" * 60)
print(f" TOOL USE AGENT ({MODEL_NAME}) ")
print("=" * 60)

print("Try:")
print(" - what time is it?")
print(" - calculate 25*12")
print(" - count words in 'Hello world!'")
print(" - give me an AI quiz")
print(" - type 'exit' to quit")

# ==============================================================================
# MAIN LOOP
# ==============================================================================

while True:

    user_input = input("\nYou: ").strip()

    if user_input.lower() == "exit":
        print("\nGoodbye!")
        break

    if not user_input:
        continue

    chat_history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = ollama.chat(
        model=MODEL_NAME,
        messages=chat_history
    )

    raw = response["message"]["content"].strip()

    print("\n[RAW MODEL OUTPUT]")
    print(raw)

    tool_used = False

    if raw.startswith("{"):

        try:

            fixed_raw = raw

            fixed_raw = fixed_raw.replace(
                "'",
                '"'
            )

            print("\n[FIXED JSON]")
            print(fixed_raw)

            call = json.loads(fixed_raw)

            tool_name = call.get("tool")
            args = call.get("args", {})

            if tool_name in TOOLS:

                print(f"\n[USING TOOL: {tool_name}]")

                tool_result = TOOLS[tool_name](**args)

                print("\n[TOOL RESULT]")
                print(tool_result)

                chat_history.append(
                    {
                        "role": "assistant",
                        "content": fixed_raw
                    }
                )

                chat_history.append(
                    {
                        "role": "user",
                        "content":
                            f"Tool result: {tool_result}. "
                            f"Now give a helpful answer."
                    }
                )

                final_response = ollama.chat(
                    model=MODEL_NAME,
                    messages=chat_history
                )

                final_reply = (
                    final_response["message"]["content"]
                )

                print(
                    "\nAgent:",
                    final_reply,
                    "\n"
                )

                chat_history.append(
                    {
                        "role": "assistant",
                        "content": final_reply
                    }
                )

                tool_used = True

        except Exception as e:

            print("\n[JSON ERROR]")
            print(str(e))

    if not tool_used:

        print("\nAgent:", raw, "\n")

        chat_history.append(
            {
                "role": "assistant",
                "content": raw
            }
        )