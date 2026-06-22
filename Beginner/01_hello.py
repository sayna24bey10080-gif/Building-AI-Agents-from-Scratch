import ollama

response = ollama.chat(
    model='tinyllama',
    messages=[
        {
            'role': 'user',
            'content': 'What is Artificial Intelligence? Explain in 3 sentences.'
        }
    ]
)

print("AI Response:")
print("-" * 40)
print(response['message']['content'])
print("-" * 40)
print("Done!")