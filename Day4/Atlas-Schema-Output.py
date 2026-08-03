from dotenv import load_dotenv
from openai import OpenAI
from colorama import init, Back, Fore
init(autoreset=True)
from pydantic import BaseModel, Field
from pydantic import ValidationError
import os
import openai
from datetime import datetime



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
        
        
def initiate_conversation() -> tuple[list[dict[str, str]], str]:
    #system_message = get_none_empty_input ("describe your asisstant")
    user_message = get_none_empty_input("give me a paragraph from which you want me to extract information for you")
    user_selection = get_none_empty_input ("What would you like to extract? \n 1. Person profile  \n 2. Team Profile \n 3. Job posting \n 4 . Meeting information \n 5 . Exit \n >>>> ")
    
    message = [
    {
        "role": "system",
        "content": (
            "Extract only information explicitly supported by the text. "
            "Do not invent missing details. Use null for missing optional "
            "fields and an empty list when no list items are given."
        ),
    },
    {
        "role": "user",
        "content": user_message,
    },
    ]
    
    return message, user_selection

class PersonProfile(BaseModel):
    name:str
    occupation: str
    location: str
    skills: list[str]
    years_of_experience : int| None = None
    confidence : float | None = Field(default = None, ge = 0.0 , le = 1.0)

class TeamProfile(BaseModel):
    team_name : str | None = None
    team_members : list [PersonProfile]
    
class MeetingInformation(BaseModel):
    meeting_title: str
    meeting_date: str | None = None
    meeting_time: str | None = None
    participants: list[str]
    location: str | None = None
    
    
class JobPosting(BaseModel):
    title: str
    company: str
    location: str | None = None
    required_skills: list[str]
    preferred_skills: list[str]
    minimum_experience_years: int | None = None
    
    
    
def ask_llm (
    client: OpenAI,
    message_history: list[dict[str,str]],
    user_selection : str,):
    
    if user_selection == "1":
        text_format = PersonProfile
    elif user_selection == "2":
        text_format = TeamProfile
    elif user_selection == "3":
        text_format = JobPosting
    elif user_selection == "4":
        text_format = MeetingInformation
    elif user_selection == "5":
        print(Fore.RED + "Exiting the program.")
        exit(0)
    else:
        print(Fore.RED + "Invalid selection")
        return None, None

    try : 
        response = client.responses.parse(model="gpt-5.6",
                                      input=message_history, 
                                      text_format=text_format)
        profile = response.output_parsed
        return profile, text_format
    
    except openai.RateLimitError as error:
        print(Fore.RED + f"Rate limit exceeded: {error}")
    
    except openai.AuthenticationError as error:
        print(Fore.RED + f"Authentication failed: {error}")
    
    except openai.APIConnectionError as error:
        print(Fore.RED + f"Could not connect to OpenAI: {error}")

    except ValidationError as error:
        print(Fore.RED + f"Invalid value provided: {error}")
        
    return None, None



def display_profile(profile) -> None:
    print("__"*50)
    print("\n\n"+Fore.BLUE + "Parsed Response:")
    print(profile)
    print("__"*50)
    print("\n\n"+Fore.GREEN + "Parsed Response as JSON:")
    print(profile.model_dump_json(indent=4))
    
    
    
def save_profile_as_json(profile, text_format) -> None:
    os.makedirs("profiles", exist_ok=True)
    # Save JSON
    profile_json = profile.model_dump_json(indent=4)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"profiles/{profile.__class__.__name__.lower()}_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(profile_json)
    print(Back.GREEN + f"profile saved as JSON in {filename}")
    
    
def main():
    load_credentials()
    llm = create_client()
    message, user_selection = initiate_conversation()
    profile, text_format = ask_llm(client=llm, message_history=message, user_selection=user_selection)
    
    if profile is not None and text_format is not None : 
        display_profile(profile = profile)
        save_profile_as_json(profile = profile, text_format = text_format)



if __name__ == "__main__":
    main()
