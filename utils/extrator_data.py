# arquivo: pesquisa.py
from typing import Dict

from selenium import webdriver
import streamlit as st
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import pandas as pd
import datetime
import os
from dotenv import load_dotenv
import logging
import xlsxwriter

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# URL do site
url_data = os.getenv("URL_DATA")
print(url_data)


def data_fetch(cpf, month_start, year_start, month_end, year_end, driver):
    try:
        data_by_year: dict[int, pd.DataFrame] = {}
        current_date = datetime.date(year_start, month_start, 1)
        end_data = datetime.date(year_end, month_end, 1)

        while current_date <= end_data:
            month = current_date.month
            year = current_date.year


            url_search = f'{url_data}?cpf={cpf}&mes={month}&ano={year}'
            driver.get(url_search)
            print(f"Ano atual: {year}")  # Verificar o valor do ano a cada iteração
            print(f"URL sendo acessada: {url_search}")  # Verificar a URL sendo usada

            try:
                table = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, "//*[@id='mesatual']/table"))
                )

                df_month = pd.read_html(table.get_attribute("outerHTML"))[0]

                # Adiciona o DataFrame do mês ao DataFrame do ano
                if year not in data_by_year:
                    data_by_year[year] = df_month
                else:
                    data_by_year[year] = pd.concat([data_by_year[year], df_month], ignore_index=True)

                print(f"Dados coletados do mês {month}/{year}:\n{df_month}\n")
                print(f"Conteúdo de data_by_year:\n{data_by_year}\n")

            except TimeoutException:
                print(f"Timeout ao carregar tabela para {month}/{year}")

            current_date += datetime.timedelta(days=32)
            current_date = current_date.replace(day=1)

        # Salva os dados em um arquivo Excel com abas por ano
        with pd.ExcelWriter(f'{cpf}.xlsx', engine='xlsxwriter') as writer:
            for year, df_year in data_by_year.items():
                df_year.to_excel(writer, sheet_name=str(year), index=False)
                workbook = writer.book
                worksheet = workbook.get_worksheet_by_name(str(year))
                worksheet.hide()
        return True

    except Exception as e:
        print(f"Erro ao gerar arquivo: {e}")
        return False


