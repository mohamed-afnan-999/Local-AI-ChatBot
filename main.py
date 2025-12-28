# implement chat history and memory
# switch models - done
# select models by number not name - done


# class LLM_Interface:
#     def __init__(self):
#         self.current_model = ''
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

def list_cloud_models():
    ollama_cloud_url = 'https://ollama.com/api/tags'
    response = requests.get(ollama_cloud_url)
    cloud_models: list = []

    if response.status_code == 200:
        cloud_models = response.json().get("models", [])
        cloud_models = [model["name"] for model in cloud_models]

    return cloud_models

def select_model():
    cloud_models: list = list_cloud_models()
    if not cloud_models:
        print("Failed to fetch list of available cloud models.")
        return None

    print(f"\nSelect one of the following models to run remotely [1 - {len(cloud_models)}]")
    for i, model_name in enumerate(cloud_models):
        print(f"{i+1}. {model_name}")
    selected_model = int(input())

    return cloud_models, cloud_models[selected_model-1]

def switch_model(running_model):
    cloud_models: list = list_cloud_models()

    '''extracting the list of available cloud models'''
    c: int = 0
    for i, model in enumerate(cloud_models):
        if model == running_model:
            cloud_models.pop(i-1)
            continue
        cloud_models[c] = [c+1, model]
        c += 1

    """user model selection"""
    for i, model in enumerate(cloud_models):
        print(f"{i+1}. {model}")
    selected_model: int = int(input("\nEnter model number: "))

    return cloud_models[selected_model-1]

def stream_response(model, messages, want_to_stream):
    client = Client(host = 'https://ollama.com', headers = {'Authorisation': 'Bearer ' + getenv('OLLAMA_API_KEY')})

    if want_to_stream.lower() in ['t', 'true', 'yes', 'y']:
        '''if response is needed to be streamed, it will be broken down token by token, word by word, hence need a for loop to capture each token/word generated'''
        for part in client.chat(model= model, messages= messages, stream= True):
            print(f"{part['message']['content']}", end="", flush= True)
    else:
        '''if no streaming is required, response is generated in one go, hence cannot use a for loop to capture the generated response'''
        response = client.chat(model= model, messages= messages, stream= False)
        print(f"{response['message']['content']}")

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
    print(f"\nType 'exit' or '/bye' to quit session.\nType 'switch' keyword to change running model.\n")

    want_to_stream = input("Do you want a streamed response to your queries? (True/False)\n")
    stream_response(model, messages, want_to_stream)

    user_input = input("\nPrompt: ")
    while user_input is not None:

        if "switch" in user_input:  # changing model
            model = switch_model(model)
            print(f"New model selected: {model}")
            user_input = input("\nPrompt: ")
            continue

        messages[0]['content'] = user_input
        stream_response(model, messages, want_to_stream)
        print()

        for exit_prompt in exit_prompts:
            if exit_prompt in user_input:
                return

        user_input = input("\nPrompt: ").lower()

if __name__ == "__main__":
    main()