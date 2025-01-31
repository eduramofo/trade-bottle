import pandas as pd
import time
import json

from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def panorama_laatus():
    df = get_data()
    return df


def get_data():

    data = {}

    # Configuração do Selenium (exemplo com Chrome)
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    # Configurando o driver do Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Executar em modo headless (sem abrir o navegador)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Inicializar o driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # URL de login
    login_url = "https://www.panoramalaatus.com.br/accounts/login/?panorama=/"

    # Abrir a página de login
    driver.get(login_url)

    # Esperar a página carregar (opcional, mas recomendável)
    time.sleep(2)

    # Localizar os campos de login e preencher
    username_field = driver.find_element(By.ID, "id_username")
    password_field = driver.find_element(By.ID, "id_password")

    username_field.send_keys(config("PANORAMA_LAATUS_USERNAME"))
    password_field.send_keys(config("PANORAMA_LAATUS_PASSWORD"))
    password_field.send_keys(Keys.RETURN)  # Simular pressionar Enter

    # Esperar o login ser processado (ajuste o tempo conforme necessário)
    time.sleep(3)

    # Verificar se o login foi bem-sucedido
    if "logout" in driver.page_source.lower():
        print("Autenticação bem-sucedida!")

        # Usar o BeautifulSoup para analisar o HTML da página
        soup = BeautifulSoup(driver.page_source, "html.parser")
        data['titulos'] = tabela_to_data(soup, 'card-6')
        data['principais'] = tabela_to_data(soup, 'card-10')
        data['nasdaq'] = tabela_to_data(soup, 'card-13')

        print("Conteúdo capturado com sucesso!")
    else:
        print("Falha na autenticação. Verifique as credenciais.")

    # Fechar o navegador
    driver.quit()

    return data


def tabela_to_data(soup, htmlId):
    table_data = []
    card = soup.find('div', id=htmlId)
    if card:
        table = card.find('table')
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            row_data = [cell.get_text(strip=True) for cell in cells]
            table_data.append(row_data)
    return process_table(table_data)


def clean_data(data):
    headers = data[0]
    df = pd.DataFrame(data[1:], columns=headers)
    df = df.iloc[:, :-1]  # Remove a última coluna
    df.columns = headers[:-1]  # Atualiza os cabeçalhos removendo o último


def gerar_arquivo(data):
    nome_arquivo = "dados.json"
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(data, arquivo, ensure_ascii=False, indent=4)
    print(f"Arquivo '{nome_arquivo}' salvo com sucesso!")


def process_table(data):
    headers = data[0]
    df = pd.DataFrame(data[1:], columns=headers)
    df = df.iloc[:, :-2].join(df.iloc[:, -1])
    df.columns = headers[:-2] + ["Data/Hora"]
    return df
