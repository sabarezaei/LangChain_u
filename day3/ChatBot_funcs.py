import os

import openai
from colorama import Fore, Back, init
from dotenv import load_dotenv
from openai import OpenAI

init(autoreset=True)


def load_credentials() -> None:
    """Load and validate the OpenAI API key."""

    env_loaded = load_dotenv()

    if not env_loaded:
        print(Fore.YELLOW + "Warning: No .env file was found.")

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY was not found. Add it to your .env file."
        )

    print(Fore.GREEN + "OpenAI API key loaded successfully.")


def create_client() -> OpenAI:
    """Create and return an OpenAI API client."""

    return OpenAI()


def get_nonempty_input(prompt: str) -> str:
    """Keep asking until the user enters nonempty text."""

    while True:
        value = input(prompt).strip()

        if value:
            return value

        print(Fore.YELLOW + "Please enter a nonempty message.")


def initialize_conversation() -> list[dict[str, str]]:
    """Create the initial system and user messages."""

    system_message = get_nonempty_input(
        "What should your assistant be like? Start with: You are a... "
    )

    initial_user_message = get_nonempty_input(
        "What is your initial message to your assistant? "
    )

    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": initial_user_message},
    ]


def ask_llm(
    client: OpenAI,
    message_history: list[dict[str, str]],
):
    """Send the conversation to the model and return its response."""

    try:
        return client.responses.create(
            model="gpt-5.6",
            input=message_history,
        )

    except openai.RateLimitError as error:
        print(Fore.RED + f"Rate limit exceeded: {error}")

    except openai.AuthenticationError as error:
        print(Fore.RED + f"Authentication failed: {error}")

    except openai.APIConnectionError as error:
        print(Fore.RED + f"Could not connect to OpenAI: {error}")

    except openai.APIStatusError as error:
        print(
            Fore.RED
            + f"OpenAI returned status {error.status_code}: {error}"
        )

    except openai.APIError as error:
        print(Fore.RED + f"OpenAI API error: {error}")

    except Exception as error:
        print(Fore.RED + f"Unexpected error: {error}")

    return None


def print_usage(response) -> None:
    """Display token usage for one API request."""

    if response.usage is None:
        print(Fore.YELLOW + "Token usage was not available.")
        return

    print(Fore.BLUE + f"Input tokens: {response.usage.input_tokens}")
    print(Fore.BLUE + f"Output tokens: {response.usage.output_tokens}")
    print(Fore.BLUE + f"Total tokens: {response.usage.total_tokens}")


def print_history(message_history: list[dict[str, str]]) -> None:
    """Pretty-print the conversation history."""

    print(Fore.CYAN + "\nConversation history:")

    for message in message_history:
        role = message["role"].capitalize()
        content = message["content"]
        print(f"\n{role}:\n{content}")


def chat(
    client: OpenAI,
    message_history: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Run the interactive chat loop."""

    while True:
        response = ask_llm(client, message_history)

        if response is None:
            retry = input(
                "Request failed. Type 'retry' or 'quit': "
            ).strip().lower()

            if retry in {"quit", "exit"}:
                break

            continue

        assistant_reply = response.output_text

        message_history.append(
            {"role": "assistant", "content": assistant_reply}
        )

        print(Fore.GREEN + f"\nAtlas: {assistant_reply}\n")
        print_usage(response)

        user_response = input("\nYou: ").strip()
        command = user_response.lower()

        if command in {"quit", "exit"}:
            print("Goodbye!")
            break

        if command == "reset":
            message_history = initialize_conversation()
            print(Fore.YELLOW + "Conversation reset.\n")
            continue

        if command == "history":
            print_history(message_history)
            continue

        if not user_response:
            print(Fore.YELLOW + "Please enter a message.")
            continue

        message_history.append(
            {"role": "user", "content": user_response}
        )

    return message_history


def main() -> None:
    """Run Atlas."""

    try:
        load_credentials()
        client = create_client()
        message_history = initialize_conversation()
        message_history = chat(client, message_history)
        print_history(message_history)

    except RuntimeError as error:
        print(Fore.RED + str(error))


if __name__ == "__main__":
    main()