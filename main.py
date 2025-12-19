


# class LLM_Interface:
#     def __init__(self):
#         pass
#
#     def load_config(self):
#         pass
#
#     def converse(self):
#         pass
#
#     def check_connection(self):
#         pass
#

from dotenv import load_dotenv
from os import getenv
from ollama import Client
import os


def configure():
    load_dotenv()

def select_model():
    ...

def main():
    configure()

    """ extracting api key from .env file """
    key = getenv('OLLAMA_API_KEY')
    print(key)

    """ Establishing connection with Ollama model and testing it."""
    client = Client(host = 'https://ollama.com', headers = {'Authorization': 'Bearer ' + os.getenv('OLLAMA_API_KEY')})

    exit_prompts = ['/bye', 'exit']

    messages = [
        {
            'role': 'user',
            'content': "You are a coding assistant that is skeptical, so you double check before answering. However, keep the answers short when short answers can suffice"
        }
    ]

    for part in client.chat('deepseek-v3.1:671b-cloud', messages= messages, stream = True):
        print(f"{part['message']['content']}", end="", flush=True)

    user_input = input("\nPrompt: ")
    while user_input not in exit_prompts or user_input is not None:

        messages[0]['content'] = user_input
        conversation = client.chat('deepseek-v3.1:671b-cloud', messages= messages, stream = True)
        for part in conversation:
            every_word = part
            print(f"{every_word['message']['content']}", end="", flush= True)
        print()
        user_input = input("Prompt: ")

    # print(f"")

if __name__ == "__main__":
    main()