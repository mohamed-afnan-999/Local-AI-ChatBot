# implement chat history and memory
# switch models
# select models by number not name


# class LLM_Interface:
#     def __init__(self):
#         self.currrent_model = ''
#         pass
#
#     def load_config(self):        from .yaml file
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
import requests

def configure():
    load_dotenv()

def select_model():
    ollama_cloud = 'https://ollama.com/api/tags'
    response = requests.get(ollama_cloud)
    selected_model = 1
    cloud_models: list = []

    if response.status_code == 200:
        cloud_models = response.json().get("models", [])
        cloud_models = [(i+1, model["name"]) for i, model in enumerate(cloud_models)]
        print(f"Select one of the following models to run remotely [1 - {len(cloud_models)}]")
        for i, model_name in cloud_models:
            print(f"{i}. {model_name}")
        selected_model = int(input())
    else:
        print("Failed to fetch cloud models.")

    return cloud_models, cloud_models[selected_model-1][1]

def switch_model(running_model):
    ollama_cloud = 'https://ollama.com/api/tags'
    response = requests.get(ollama_cloud)
    cloud_models: list = []

    '''extracting the list of available cloud models'''
    if response.status_code == 200:
        cloud_models = response.json().get("models", [])
        cloud_models = [(i+1, model["name"]) for i, model in enumerate(cloud_models)]

        c: int = 0
        for i, model in cloud_models:
            if model == running_model:
                cloud_models.pop(i-1)
                continue
            cloud_models[c] = [c+1, model]
            c += 1

    """user model selection"""
    for i, model in cloud_models:
        print(f"{i}. {model}")
    selected_model: int = int(input("\nEnter model number: "))

    return cloud_models[selected_model-1][1]

def main():
    configure()

    """ extracting api key from .env file """
    key = getenv('OLLAMA_API_KEY')

    """ Establishing connection with Ollama model and testing it."""
    client = Client(host = 'https://ollama.com', headers = {'Authorization': 'Bearer ' + key})

    exit_prompts = ['/bye', 'exit']

    messages = [
        {
            'role': 'user',
            'content': "You are a coding assistant that is skeptical, so you double check before answering. However, keep the answers short when short answers can suffice"
        }
    ]

    _, model = select_model()
    print(f"Model currently in use is {model}.")

    for part in client.chat(model, messages= messages, stream = True):
        print(f"{part['message']['content']}", end="", flush=True)
        print(f"\nType 'exit' or '/bye' to quit session.\nType 'switch' keyword to change running model.")

    user_input = input("\nPrompt: ")
    while user_input not in exit_prompts or user_input is not None:

        if "switch" in user_input:  # changing model
            model = switch_model(model)
            print(f"New model selected: {model}")
            user_input = input("Prompt: ")
            continue

        messages[0]['content'] = user_input
        conversation = client.chat(model, messages= messages, stream = True)
        for part in conversation:
            every_word = part
            print(f"{every_word['message']['content']}", end="", flush= True)
        print()
        user_input = input("Prompt: ").lower()

if __name__ == "__main__":
    main()