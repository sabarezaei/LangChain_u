from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


llm = OpenAI()

responce = llm.responses.create(model = "gpt-5.6", input = "what country has the tallest mountains?")


print(f"\n Model : {responce.model},\n Output Text : {responce.output_text}, \n Usage : {responce.usage}")

print(f"Input tokens: {responce.usage.input_tokens}")
print(f"Output tokens: {responce.usage.output_tokens}")
print(f"Total tokens: {responce.usage.total_tokens}")