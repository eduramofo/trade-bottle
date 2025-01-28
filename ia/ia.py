import json
from openai import OpenAI
from decouple import config


def ia(file_path):
    client = OpenAI(api_key=config("OPENAI_API_KEY"))
    chat_completion = client.chat.completions.create(messages=get_messages(file_path), model="gpt-4o")
    message_content = chat_completion.choices[0].message.content
    message_content_save(message_content)


def get_messages(file_path):
    message1 = {"role": "system", "content": system()}
    message2 = {"role": "user", "content": prompt(file_path)}
    return [message1, message2]


def system():
    text = """
    Você é um day trader senior.
    Faça uma análise resumida do índice US 10Y e do VIX.
    """
    return text


def prompt(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    prompt = json.dumps(data, indent=2)
    return prompt


def message_content_save(content):
    file_name = "análise.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Dados salvos no arquivo {file_name}")
