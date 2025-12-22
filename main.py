


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
import requests

def configure():
    load_dotenv()

def select_model():
    ollama_cloud = 'https://ollama.com/api/tags'
    response = requests.get(ollama_cloud)
    selected_model = "deepseek-v3.1:671b-cloud"

    if response.status_code == 200:
        cloud_models = response.json().get("models", [])
        print("Select one of the following models to run remotely")
        for i, model in enumerate(cloud_models):
            print(f"{i+1}. {model["name"]}")
        selected_model = input()
    else:
        print("Failed to fetch cloud models.")

    return selected_model

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

    model: str = select_model()
    print(f"Model currently in use is {model}.")

    for part in client.chat(model, messages= messages, stream = True):
        print(f"{part['message']['content']}", end="", flush=True)

    user_input = input("\nPrompt: ")
    while user_input not in exit_prompts or user_input is not None:

        messages[0]['content'] = user_input
        conversation = client.chat(model, messages= messages, stream = True)
        for part in conversation:
            every_word = part
            print(f"{every_word['message']['content']}", end="", flush= True)
        print()
        user_input = input("Prompt: ")

    # print(f"")

if __name__ == "__main__":
    main()