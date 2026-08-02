from openai import OpenAI
from pydantic import BaseModel


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


client = OpenAI()

response = client.responses.parse(
    model="gpt-5.6",
    input=[
        {
            "role": "system",
            "content": "Extract the event information.",
        },
        {
            "role": "user",
            "content": (
                "Alice and Bob are going to a science fair on Friday."
            ),
        },
    ],
    text_format=CalendarEvent,
)

event = response.output_parsed

if event is None:
    raise RuntimeError("The response could not be parsed.")

print(event.name)
print(event.date)
print(event.participants)