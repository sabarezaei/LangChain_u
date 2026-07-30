import os

import openai
from colorama import Fore, Back, init
from dotenv import load_dotenv
from openai import OpenAI

init(autoreset=True)


def load_credentials() -> None:
    """Loading the API KEYS"""
    
    
    load_env = load_dotenv()   # it returns True or False
    if not load_env:
        print(Fore.RED + ">>>>>>>>>>>>>>>>   Error : .env file not found")
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        raise RuntimeError(
            "OPENAI_API_KEY was not found. Add it to your .env file."
        )
    else :
        print(Back.GREEN + "OpenAI API key loaded successfully.")



def create_client() -> OpenAI:
    """Making an instance of the LLM"""

    return OpenAI()




def handle_empty_responces (prompt : str) -> str:
    while True:
        resp = input(prompt).strip()
        if resp:
            return resp
        
        print(Back.YELLOW + "please enter non-empty input")
        

        

def initialize_conversation() -> list[dict[str, str]]:
    
    system_message= handle_empty_responces(prompt = "What do you want your assistant to be like? Start with: You are a... ")
    
    initial_user_message = handle_empty_responces(prompt = "What is your initial message to your assistant? ")
    
    message_history = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": initial_user_message},
        ]
    return message_history



def ask_llm(
    client: OpenAI, 
    message_history : list[dict[str, str]]
    ):
    
    try :
        response = client.responses.create(
                model="gpt-5.6",
                input=message_history,
            )
    except openai.RateLimitError as e:
        #Handle API error here, e.g. retry or log
        print(Fore.RED + f"OpenAI API returned an API Error: {e}")
        return None
    except openai.APIConnectionError as e:
        #Handle connection error here
        print(Fore.RED + f"Failed to connect to OpenAI API: {e}")
        return None
    except openai.APIStatusError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        print(Fore.RED + f"OpenAI API request exceeded rate limit: {e}")
        return None
    except Exception as e:
        print(Fore.RED + str (e))
        return None
    
    assistant_reply = response.output_text
    
    message_history.append(
            {"role": "assistant", "content": assistant_reply}
        )
    
    print(Fore.GREEN + f"\nAtlas: {assistant_reply}\n")
    
    return message_history, response


def print_usage(response) -> None:
    if response is None:
        raise ValueError("response cannot be None")
    
    
    print(Fore.BLUE + f"Input tokens: {response.usage.input_tokens}")
    print(Fore.BLUE + f"Output tokens: {response.usage.output_tokens}")
    print(Fore.BLUE + f"Total tokens: {response.usage.total_tokens}")

def pretty_print_histort (message_history : list[dict[str,str]]) -> None :
    """Pretty-print the conversation history."""
    for message in message_history:
        print("\n\n"+ Fore.YELLOW + message['role'].upper())
        print("\n" + Fore.GREEN + message['content'])
        
        
        
        
def chat (client: OpenAI, message_history: list[dict[str, str]]) -> list[dict[str, str]]:
    
    while True:
        message_history, responce = ask_llm(client,message_history)
        print_usage(responce)
        user_response = input("What do you think: ").strip()

        if user_response.lower() in {"quit", "exit"}:
            print("Goodbye!")
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

    return message_history



def main (): 
    try: 
        load_credentials()
        client= create_client()
        message_history = initialize_conversation()

        cmessage_history = chat(
        client=client,
        message_history=message_history,
        )
        pretty_print_histort(message_history=message_history)
    except RuntimeError as error:
            print(Fore.RED + str(error))
        
    
        
        
if __name__ == "__main__":
    main()