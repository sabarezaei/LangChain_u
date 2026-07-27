


import openai
from openai import OpenAI
client = OpenAI()

try:
  #Make your OpenAI API request here
  response = client.responses.create(
    model="gpt-5.6",
    input="Hello world"
  )
except openai.APIError as e:
  #Handle API error here, e.g. retry or log
  print(f"OpenAI API returned an API Error: {e}")
  pass
except openai.APIConnectionError as e:
  #Handle connection error here
  print(f"Failed to connect to OpenAI API: {e}")
  pass
except openai.RateLimitError as e:
  #Handle rate limit error (we recommend using exponential backoff)
  print(f"OpenAI API request exceeded rate limit: {e}")
  pass

from colorama import Fore, Back, Style, init

# Initialize colorama (autoreset automatically reverts color after each print)
init(autoreset=True)

print(Fore.RED + "Red text")
print(Fore.GREEN + "Green text")
print(Back.YELLOW + Fore.BLACK + "Black text on a Yellow background")
print(Style.BRIGHT + Fore.BLUE + "Bright Blue text")
