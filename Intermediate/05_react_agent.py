import ollama

REACT_SYSTEM = """
You are ReAct (Reasoning + Acting) AI Agent.

For EVERY question, you MUST respond using this exact format - never skip a step:

THOUGHT: [Analyze what the question is really asking. What do you know about this topic?]

PLAN: [Describe your step-by-step approach to answer this well.]

ACTION: [Execute your plan. Work through the answer in detail. Show your thinking.]

FINAL ANSWER: [Write a clear, concise summary answer in 2-3 sentences maximum.]

Rules:
- Never answer directly without going through all 4 steps
- Thought must be at least 2 sentences
- Action must show actual work/reasoning
- Final answer must be short and clear
"""

chat_history = [{"role": "system", "content": REACT_SYSTEM}]

print("=" * 50)
print("  ReAct Reasoning Agent (TinyLlama)")
print("=" * 50)
print("I reason through every question step by step.")
print("Type 'exit' to quit.\n")

question_num = 0

while True:
    question = input("Ask me: ").strip()

    if question.lower() == "exit":
        print(f"\nSession ended. You asked {question_num} questions.")
        break

    if not question:
        continue

    question_num += 1

    chat_history.append({
        "role": "user",
        "content": question
    })

    print(f"\n{'=' * 50}")
    print(f"Question #{question_num}: {question}")
    print(f"{'=' * 50}")
    print("Agent is reasoning...\n")

    try:
        response = ollama.chat(
            model="tinyllama",
            messages=chat_history
        )

        answer = response["message"]["content"]

        print(answer)
        print(f"\n{'=' * 50}\n")

        chat_history.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as e:
        print(f"Error: {e}")

      