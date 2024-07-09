# arquivo: pesquisa.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import datetime
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# URL do site
url_base = os.getenv("URL_BASE")
url_pesquisa = f"{url_base}/pesquisa"


def data_fetch(month_start, year_start, month_end, year_end):
    # Configuração do WebDriver
    options = webdriver.ChromeOptions()
    # Executa o Chrome em modo headless
    # options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)

    try:
        date_start = datetime.date(year_start, month_start, 1)
        date_end = datetime.date(year_end, month_end, 1)
        data_by_month = {}
        current_date = date_start

        while current_date <= date_end:
            month = current_date.month
            year = current_date.year
            url_search = f"{url_pesquisa}?mes={mes}&ano={ano}"  # Adapte os parâmetros da URL conforme necessário
            driver.get(url_completa)

            # Timeout explícito para carregar a tabela
            try:
                tabela = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "table#tabela-resultados"))
                )
                df = pd.read_html(tabela.get_attribute("outerHTML"))[0]
                dados_por_mes[f"{mes:02d}/{ano}"] = df
            except TimeoutException:
                print(f"Timeout ao carregar tabela para {mes}/{ano}")

            data_atual += datetime.timedelta(days=32)
            data_atual = data_atual.replace(day=1)

        # Salva os dados após o término da coleta
        with pd.ExcelWriter("dados_pesquisa.xlsx") as writer:
            for mes_ano, dados in dados_por_mes.items():
                dados.to_excel(writer, sheet_name=mes_ano, index=False)
        return True

    except Exception as e:
        print(f"Erro ao realizar pesquisa: {e}")
        return False
    finally:
        driver.quit()