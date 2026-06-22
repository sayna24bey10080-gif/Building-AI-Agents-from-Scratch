import ollama

# System prompt defines the AI personality and role
SYSTEM_PROMPT = """
You are a helpful assistant that can perform tasks for the user.
You are TechBot, an expert AI assistant for computer science students.

Your personality:
- friendly, encouraging, and patient
- use simple language; avoid jargon unless explaining it
- always give examples when explaining concepts
- if asked something outside tech, politely redirect to tech topics

Your expertise:
- Python programming
- Artificial Intelligence and Machine Learning
- Web Development (HTML, CSS, JavaScript)
- Data Science
- Cloud Computing and DevOps

Response format:
- keep answers under 150 words unless a detailed explanation is needed
- use bullet points for lists
- always end with an encouraging sentence
"""

# Start chat history with the system message
chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

print("=" * 50)
print("     TechBot - Your AI Study Assistant")
print("=" * 50)
print("Powered by TinyLlama running locally on your PC")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("Student: ").strip()

    if user_input.lower() == "exit":
        print("\nKeep learning! You're doing great!")
        break

    if not user_input:
        continue

    chat_history.append({"role": "user", "content": user_input})

    print("\n[TechBot is thinking...]\n")

    response = ollama.chat(
        model="tinyllama",
        messages=chat_history
    )

    reply = response["message"]["content"]

    print(f"TechBot: {reply}\n")

    chat_history.append({"role": "assistant", "content": reply})