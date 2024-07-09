# arquivo: pesquisa.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import pandas as pd
import datetime
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# URL do site
url_data = os.getenv("URL_DATA")


def data_fetch(cpf, month_start, year_start, month_end, year_end):
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

            url_search = f"{url_data}?cpf={cpf}&mes={month}&ano={year}"
            driver.get(url_search)

            # Timeout explícito para carregar a tabela
            try:
                table = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, "//*[@id='mesatual']/table"))
                )
                df = pd.read_html(table.get_attribute("outerHTML"))[0]
                data_by_month[f"{month:02d}/{year}"] = df
            except TimeoutException:
                print(f"Timeout ao carregar tabela para {month}/{year}")

            current_date += datetime.timedelta(days=32)
            current_date = current_date.replace(day=1)

        # Salva os dados após o término da coleta
        with pd.ExcelWriter("dados_pesquisa.xlsx") as writer:
            for month_year, data in data_by_month.items():
                data.to_excel(writer, sheet_name=month_year, index=False)
        return True

    except Exception as e:
        print(f"Erro ao realizar pesquisa: {e}")
        return False
    finally:
        driver.quit()
