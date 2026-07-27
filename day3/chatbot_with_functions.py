from dotenv import load_dotenv

from colorama import Fore, Back, Style, init
init(autoreset=True)

from openai import OpenAI
import os


def load_credentials():
    
    """Loading the API KEYS"""
    try: 
        load_dotenv()
    except:
        print(Fore.RED + ">>>>>>>>>>>>>>>>   Error : .env file not found")
    
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        print(Back.YELLOW + openai_api_key)
    except:
        print("\n Error : OpenAI API key Not Found in the .env file")



def create_client():
    """MAking an instance of the LLM"""
    
    C1 = OpenAI()
    return C1



def initialize_conversation():
    system_message= ""
    while system_message == "":
        system_message = input(
        "What do you want your assistant to be like? Start with: You are a... "
        ).strip()
    
    initial_user_message = ""    
    while initial_user_message =="" :
        initial_user_message = input(
        "What is your initial message to your assistant? "
        ).strip()
    
    message_history = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": initial_user_message},
        ]
    return message_history



def ask_llm(client, message_history):
    
    try :
        response = client.responses.create(
                model="gpt-5.6",
                input=message_history,
            )
    except openai.APIError as e:
        #Handle API error here, e.g. retry or log
        print(Fore.RED + f"OpenAI API returned an API Error: {e}")
        pass
    except openai.APIConnectionError as e:
        #Handle connection error here
        print(Fore.RED + f"Failed to connect to OpenAI API: {e}")
        pass
    except openai.RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        print(Fore.RED + f"OpenAI API request exceeded rate limit: {e}")
        pass
    except Exception as e:
        print(Fore.RED + str (e))
        pass
    
    assistant_reply = response.output_text
    
    message_history.append(
            {"role": "assistant", "content": assistant_reply}
        )
    
    print(Fore.GREEN + f"\nAtlas: {assistant_reply}\n")
    
    return message_history, response


def print_usage(assistant_reply):
    print(Fore.BLUE + f"Input tokens: {assistant_reply.usage.input_tokens}")
    print(Fore.BLUE + f"Output tokens: {assistant_reply.usage.output_tokens}")
    print(Fore.BLUE + f"Total tokens: {assistant_reply.usage.total_tokens}")


def chat (client, message_history):
    MORE_QUESTIONS = True
    while MORE_QUESTIONS:
        message_history, responce = ask_llm(client,message_history)
        print_usage(responce)
        user_response = input("What do you think: ").strip()

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

    return message_history



if __name__ == "__main__": 
    load_credentials()
    client= create_client()
    message_history = initialize_conversation()

    chat(client=client, message_history=message_history)


    print("\nFinal message history:")
    for message in message_history:
        print(f"\n\n{message['role'].upper()}: \n {message['content']}")