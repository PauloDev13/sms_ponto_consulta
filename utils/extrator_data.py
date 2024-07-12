# arquivo: pesquisa.py
import streamlit as st

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

import pandas as pd
from bs4 import BeautifulSoup

import os
from io import StringIO
from time import sleep
import xlsxwriter
import logging
import datetime
from dotenv import load_dotenv

from utils import utils

# Formata as mensagens de log
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Carrega o arquivo .env
load_dotenv()

# Ler a URL base que vai montar a busca dos dados
url_data = os.getenv('URL_DATA')
file_path = os.getenv('PATH_FILE_BASE')


def data_fetch(cpf, month_start, year_start, month_end, year_end, driver):
    try:
        # Atribui variáveis para receber o conjunto de dados (dicionário)
        # e as datas do intervalo a ser pesquisado
        data_by_year: dict[int, pd.DataFrame] = {}
        current_date = datetime.date(year_start, month_start, 1)
        end_date = datetime.date(year_end, month_end, 1)

        # Enquanto a data inicial for menor que a data final,
        # é extraído o mês e o ano das datas informadas
        while current_date <= end_date:
            month = current_date.month
            year = current_date.year

            # Monta e atribui a variável 'table' a URL com os query params
            # da pesquisa e abre no navegador
            url_search = f'{url_data}?cpf={cpf}&mes={month}&ano={year}'
            driver.get(url_search)

            try:
                # Verifica se o elemento HTML contém a tag
                WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[4]/div/span/font[1]")
                    )
                )
                # Procura e atribui a variável 'employee_name' o conteúdo da tag
                employee_name = driver.find_element(
                    By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[4]/div/span/font[1]"
                ).text
                # Verifica se o elemento HTML contém a tag table
                table = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, "//*[@id='mesatual']/table"))
                )

                # Utiliza a biblioteca BeautifulSoup para analisar o HTML da tabela
                # e atribui o resultado à variável 'soup'
                soup_table = BeautifulSoup(table.get_attribute("outerHTML"), 'html.parser')

                # Utiliza a biblioteca Pandas para montar um DataFrame com os dados
                # da primeira tabela encontrada no HTML
                df_month = pd.read_html(StringIO(str(soup_table)))[0]


                # Adiciona a linha separadora ao DataFrame do mês
                # df_month = pd.concat([df_separator, df_month], ignore_index=True)

                # Se o ano não existir dentro do DataFrame 'data_by_year',
                # adiciona-o, caso contrário concatena com o conteúdo já existente
                if year not in data_by_year:
                    data_by_year[year] = df_month
                else:
                    # Cria as linhas a serem inseridas
                    # Cria no DataFrame uma linha com mês/ano que será inserida
                    # separando os dados de cada mês
                    empty_row = pd.DataFrame([[''] * len(df_month.columns)], columns=df_month.columns)

                    employee_row = f'Detalhamento do Ponto Digital - {employee_name} - {month:02d}/{year}'
                    data_employee_row = pd.DataFrame([[employee_row] + [''] * (df_month.shape[1] - 1)],
                                                columns=df_month.columns)

                    header_row = pd.DataFrame([df_month.columns], columns=df_month.columns)

                    # Concatena as linhas com o DataFrame do mês atual
                    data_by_year[year] = pd.concat(
                        [data_by_year[year], empty_row, data_employee_row, header_row, df_month], ignore_index=True)


            # Se ocorrer erro durante o processo de coleta e montagem de dados no DataFrame,
            # exibe mensagem de erro, espera 2 segundos e fecha a mensagem
            except TimeoutException:
                utils.default_msg(
                    f'Erro ao montar dados carregados da tabela para {month}/{year}', 'error')

            current_date += datetime.timedelta(days=32)
            current_date = current_date.replace(day=1)

        # Depuração: Imprime o conteúdo do dicionário data_by_year
        for year, df in data_by_year.items():
            print(f"Ano: {year}, Número de Linhas: {len(df)}")

        # Itera sobre as chaves (anos) e valores (DataFrames) do dicionário
        # e cria o arquivo excel com os dados agrupados por ano em cada aba e salva na pasta BOT
        with pd.ExcelWriter(fr'{file_path}\{employee_name}_{cpf}.xlsx', engine='xlsxwriter') as writer:
            for year, df_year in data_by_year.items():
                df_year.to_excel(writer, sheet_name=str(year), index=False, startrow=0)
                workbook = writer.book
                worksheet = writer.sheets[str(year)]

        # Retorna verdadeiro se toda operação foi realizada com sucesso
        return True

    # Se ocorrer erro durante o processo, exibe mensagem,
    # espera 2 segundos e fecha a mensagem
    except Exception as e:
        utils.default_msg('Erro ao gerar arquivo!', 'error')

        print(f'Erro ao gerar arquivo: {e}')

        # Retorna falso em caso de erro
        return False


