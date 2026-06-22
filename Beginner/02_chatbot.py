import ollama

print("=" * 45)
print(" TinyLlama Chatbot ")
print("=" * 45)
print("Type your questions and press Enter.")
print("Type 'exit' to quit.\n")

message_count = 0

while True:

    # get input from user
    user_input = input("You: ").strip()

    # exit condition
    if user_input.lower() in ["exit", "quit", "bye"]:
        print(f"\nGoodbye! You asked {message_count} questions.")
        break

    # skip empty input
    if not user_input:
        print("Please type something!\n")
        continue

    message_count += 1

    print(f"\n[Thinking... message #{message_count}]\n")

    # send to TinyLlama
    response = ollama.chat(
        model="tinyllama",
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    ai_reply = response["message"]["content"]

    print("AI:", ai_reply)
    print()