import openai
import os
import yaml

def load_api_key() -> str:
    """
    Load the OpenAI API key from the configuration file.
    """
    config_path = os.path.expanduser('~/.config/genie.yaml')
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    api_key = config.get('openai_api_key')
    if not api_key:
        raise ValueError("OpenAI API key not found in configuration file.")
    return api_key

def generate_commit_message(diff: str) -> str:
    """
    Send the Git diff to OpenAI's GPT model and receive a commit message.
    """
    openai.api_key = load_api_key()

    messages = [
        {"role": "system", "content": "You are an assistant that generates concise and informative Git commit messages in the imperative mood."},
        {"role": "user", "content": f"Generate a commit message for the following Git diff:\n\n{diff}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=150,
        temperature=0.5,
    )

    commit_message = response.choices[0].message.content.strip()
    return commit_message