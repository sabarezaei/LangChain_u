from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

system_message = input(
    "What do you want your assistant to be like? Start with: You are a... "
).strip()

initial_user_message = input(
    "What is your initial message to your assistant? "
).strip()

message_history = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": initial_user_message},
]

MORE_QUESTIONS = True

while MORE_QUESTIONS:
    response = client.responses.create(
        model="gpt-5.6",
        input=message_history,
    )

    assistant_reply = response.output_text

    message_history.append(
        {"role": "assistant", "content": assistant_reply}
    )

    print(f"\nAtlas: {assistant_reply}\n")

    user_response = input("You: ").strip()

    if user_response.lower() in {"quit", "exit"}:
        print("Goodbye!")
        MORE_QUESTIONS = False
        break

    if user_response.lower() == "reset":
        system_message = input(
            "New assistant behavior: You are a... "
        ).strip()

        initial_user_message = input(
            "Enter your first message: "
        ).strip()

        message_history = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": initial_user_message},
        ]

        print("Conversation reset.\n")
        continue

    if not user_response:
        print("Please enter a message.")
        continue

    message_history.append(
        {"role": "user", "content": user_response}
    )

print("\nFinal message history:")
for message in message_history:
    print(f"{message['role'].upper()}: {message['content']}")