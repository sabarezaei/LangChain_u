from dotenv import load_dotenv
from openai import OpenAI
from colorama import init, Back, Fore
from pydantic import BaseModel
import os

def load_credentials () -> None:
    env_var = load_dotenv()
    
    if not env_var:
        raise RuntimeError(".env file not found")
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key is None: 
        raise RuntimeError("API KEY not found")
    
    print(Fore.GREEN + "API KEY was sucessfully loaded")
    
    
def create_client() -> OpenAI:
    return OpenAI()

def get_none_empty_input (prompt) -> str:
    while True:
        answer = input(prompt).strip()
        if answer:
            return answer
        
        print(Fore.RED + "please input a none-empty answer")
        
        
def initiate_conversation() -> list[dict[str, str]]:
    system_message = get_none_empty_input ("describe your asisstant")
    user_message = get_none_empty_input("give me a paragraph from which you want me to extract information for you")
    
    message = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_message},
    ]


    return message

class PersonProfile(BaseModel):
    name:str
    occupation: str
    location: str
    skills: list[str]
    years_of_experience : int| None
    
    
def ask_llm (client: OpenAI, message_history: list[dict[str,str]]) -> list[dict[str,str]]:
    response = client.responses.parse(model="gpt-5.6",
                                      input=message_history, 
                                      text_format=PersonProfile)
    
    return response


def main():
    load_credentials()
    llm = create_client()
    message = initiate_conversation()
    response = ask_llm(client=llm, message_history=message)
    
    print(response.output_text)
    print(response.output_parsed)
    print(type(response.output_parsed))
    
    
    
if __name__ == "__main__":
    main()