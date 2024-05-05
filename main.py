"""Interactive demo of finetuned model"""
from client import client

while True:
    prompt = input("You: ")
    completion = client.chat.completions.create(
        messages = [
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model="ft:gpt-3.5-turbo-0125:personal:uwindsor-chatbot:9KCfqhwT",
    )
    print("Assistant:", completion.choices[0].message.content.strip())
