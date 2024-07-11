# arquivo: pesquisa.py
import streamlit as st

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

import pandas as pd
from bs4 import BeautifulSoup

from time import sleep
from io import StringIO
from dotenv import load_dotenv
import os
import datetime
import logging
import xlsxwriter

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# URL do site
url_data = os.getenv("URL_DATA")
print(url_data)


def data_fetch(cpf, month_start, year_start, month_end, year_end, driver):
    try:
        data_by_year: dict[int, pd.DataFrame] = {}
        current_date = datetime.date(year_start, month_start, 1)
        end_date = datetime.date(year_end, month_end, 1)

        while current_date <= end_date:
            month = current_date.month
            year = current_date.year

            url_search = f'{url_data}cpf={cpf}&mes={month}&ano={year}'
            driver.get(url_search)

            try:
                table = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, "//*[@id='mesatual']/table"))
                )

                # df_month = pd.read_html(BytesIO(table.get_attribute("outerHTML")))[0]
                # Utiliza BeautifulSoup para analisar o HTML da tabela
                soup = BeautifulSoup(table.get_attribute("outerHTML"), 'html.parser')

                # Utiliza Pandas para ler a tabela HTML em um DataFrame
                df_month = pd.read_html(StringIO(str(soup)))[0]

                # Cria uma linha com o nome do mês/ano
                month_year_label = f'PONTO ELETRÔNICO MÊS/ANO: {month:02d}/{year}'
                df_separator = pd.DataFrame([[month_year_label] + [''] * (df_month.shape[1] - 1)],
                                            columns=df_month.columns)

                # Adiciona a linha separadora ao DataFrame do mês
                df_month = pd.concat([df_separator, df_month], ignore_index=True)

                # Adiciona o DataFrame do mês ao DataFrame do ano
                if year not in data_by_year:
                    data_by_year[year] = df_month
                else:
                    data_by_year[year] = pd.concat([data_by_year[year], df_month], ignore_index=True)

            except TimeoutException:
                error = st.error(f'Erro ao montar dados carregados da tabela para {month}/{year}')
                sleep(2)
                error.empty()

                print(f'Erro ao montar dados carregados da tabela para {month}/{year}')

            current_date += datetime.timedelta(days=32)
            current_date = current_date.replace(day=1)

        # Depuração: Imprime o conteúdo do dicionário data_by_year
        for year, df in data_by_year.items():
            print(f"Ano: {year}, Número de Linhas: {len(df)}")

        # Salva os dados em um arquivo Excel com abas por ano
        with pd.ExcelWriter(fr'C:\Users\prmorais\Desktop\BOT\{cpf}.xlsx', engine='xlsxwriter') as writer:
            # Itera sobre as chaves (anos) e valores (DataFrames) do dicionário:
            for year, df_year in data_by_year.items():
                df_year.to_excel(writer, sheet_name=str(year), index=False, startrow=1)
                workbook = writer.book
                worksheet = writer.sheets[str(year)]

                # Encontra a linha com o mês/ano
                # separator_index = df_year.index[df_year.iloc[:, 0].str.contains(r'\d{2}/\d{4}', na=False)].tolist()[
                #                       0] + 1
                #
                # # Mescla a célula com o mês/ano
                # merge_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
                # worksheet.merge_range(f'A{separator_index + 1}:G{separator_index + 1}',
                #                       df_year.iloc[separator_index, 0], merge_format)

        return True

    except Exception as e:
        error = st.error(f'Erro ao gerar arquivo: {e}')
        sleep(2)
        error.empty()

        print(f'Erro ao gerar arquivo: {e}')
        return False


