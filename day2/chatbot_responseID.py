from dotenv import load_dotenv

load_dotenv()


from openai import OpenAI

client = OpenAI()

more_questions = True
resp_ID = None
developer_input = "Talk like a pirate."

while more_questions:
    human_input = input("What is your message for AI? ")
    if human_input == "quit":
        more_questions = False
        break

    response = client.responses.create(
        model="gpt-5.6",
        input=[
            {
                "role": "developer",
                "content": developer_input,
            },
            {
                "role": "user",
                "content": human_input,
            },
        ],
        previous_response_id=resp_ID,
    )
    resp_ID = response.id
    print(response.output_text)
        
