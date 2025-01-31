import json
from datetime import datetime, timedelta
from app.models import History


def history_select(identifier):
    order_by = History.created_on.desc()
    where = (History.created_on >= (datetime.now() - timedelta(minutes=10))) & (History.identifier == identifier)
    select = History.select().where(where).order_by(order_by).limit(5)
    return select


def get_processed_data(identifier):
    hs = history_select(identifier)
    processed_data = []
    for h in hs:
        try:
            data = json.loads(h.data)
            if isinstance(data, list):
                processed_data.extend(data)
        except json.JSONDecodeError:
            print(f"Erro ao decodificar JSON para {h.identifier}")
    return processed_data


def get_all_data():
    principais = get_processed_data("principais")
    titulos = get_processed_data("titulos")
    nasdaq = get_processed_data("nasdaq")
    data = {
        "principais": principais,
        "titulos": titulos,
        "nasdaq": nasdaq
    }
    json_compactado = json.dumps(data, separators=(',', ':'))
    return json_compactado


def prompt():
    data = get_all_data()
    prompt_string = f"""
    TAREFA:
        - Com base nos dados fornecidos no final do texto, analise o comportamento do mercado e classifique o NASDAQ seguindo as regras abaixo.
    REGRAS:
        - Considere apenas os seguintes índices:
            - Ações de Empresas: Apple (AAPL), Microsoft (MSFT) e Nvidia (NVDA)
            - Títulos: VIX e US 10Y
    PESOS:
        - A Nvidia (NVDA) tem um peso 15% maior que Apple (AAPL) e Microsoft (MSFT).
    OBJETIVO:
        Classifique o mercado (NASDAQ) em uma das seguintes tendências:
            - Lateral (sem direção clara)
            - Comprador (tendência de alta)
            - Vendedor (tendência de baixa)
    RESULTADO:
        - O resultado deve ser apresentando da seguinte forma, nome da tendência e um resumo mutio curto do motivo dessa tendência.
    DADOS:
    {data}
    """
    return prompt_string
