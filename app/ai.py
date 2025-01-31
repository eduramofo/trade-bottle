from openai import OpenAI
from decouple import config
from app.prompt import prompt
from app.models import Analysis


def ai():
    client = OpenAI(api_key=config("OPENAI_API_KEY"))
    chat_completion = client.chat.completions.create(messages=get_messages(), model="gpt-4o")
    message_content = chat_completion.choices[0].message.content
    save(message_content)


def get_messages():
    message1 = {"role": "system", "content": system()}
    message2 = {"role": "user", "content": prompt()}
    return [message1, message2]


def system():
    text = """
    Você é um day trader senior.
    Faça uma análise resumida do índice US 10Y e do VIX.
    """
    return text


def save(content):
    Analysis.create(content=content)
    print('Análise salva com sucesso!')

