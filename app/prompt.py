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
    data = {
        "principais": principais,
        "titulos": titulos
    }
    json_compactado = json.dumps(data, separators=(',', ':'))
    return json_compactado


def prompt():
    data = get_all_data()
    prompt_string = f"""
    Com base nos seguintes dados de mercado, determine a tendência do rendimento do título do Tesouro Americano de 10 anos (US 10Y). Considere principalmente a relação entre o US 10Y e o VIX, além de outros índices relevantes, como S&P500, DXY e commodities.

    Os dados são atualizados a cada 5 minutos e possuem granularidade de 1 em 1 minuto.

    Critérios de análise:
    - US 10Y subindo e VIX caindo: Indica apetite ao risco, mercado comprador e menor aversão ao risco.
    - US 10Y caindo e VIX subindo: Indica aversão ao risco, mercado vendedor, com possível busca por ativos mais seguros.
    - US 10Y e VIX subindo juntos: Pode indicar incerteza no mercado e expectativa de alta de juros ou risco elevado.
    - US 10Y e VIX caindo juntos: Pode sugerir um mercado mais estável, com menor volatilidade e possível acomodação dos juros.
    - Correlação com DXY e S&P500: Um dólar forte (DXY subindo) pode pressionar o US 10Y para cima, enquanto um S&P500 em alta pode indicar maior apetite ao risco.


    Com esses critérios, avalie se o mercado está:
    - Constante: Sem grandes oscilações, variação limitada nos rendimentos.
    - Comprador: Apetite por risco, investidores saindo dos títulos e migrando para ações/ativos de maior risco.
    - Vendedor: Avançando para ativos mais seguros, aumento na busca por títulos do Tesouro e aversão ao risco.

    Dados:
    {data}
    """
    return prompt_string
