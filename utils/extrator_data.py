# arquivo: pesquisa.py
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
from openpyxl import Workbook

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# URL do site
url_data = os.getenv("URL_DATA")
print(url_data)


def data_fetch(cpf, month_start, year_start, month_end, year_end, driver):

    # Configuração do WebDriver
    # options = webdriver.ChromeOptions()
    # Executa o Chrome em modo headless
    # options.add_argument("--headless=new")

    # driver = webdriver.Chrome(options=options)

    try:
        date_start = datetime.date(year_start, month_start, 1)
        date_end = datetime.date(year_end, month_end, 1)
        data_by_month = {}
        current_date = date_start

        print(current_date, date_end)

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
                data_by_month[f"{month:02d}-{year}"] = df
            except TimeoutException:
                print(f"Timeout ao carregar tabela para {month}/{year}")

            current_date += datetime.timedelta(days=32)
            current_date = current_date.replace(day=1)

            # Agrupa os dados por ano
            data_by_year = {}

            # Salva os dados no arquivo Excel, organizados por ano
            dir_downloads = os.path.expanduser("~/Downloads")
            path_file = os.path.join(dir_downloads, f"{cpf}.xlsx")

            wb = Workbook()
            wb.save(path_file)


            for data_str, df in data_by_month.items():
                year = data_str.split('-')[1]
                if year not in data_by_year:
                    data_by_year[year] = {}
                data_by_year[year][data_str] = df

        # Salva os dados após o término da coleta
            with pd.ExcelWriter(path_file,  engine='openpyxl') as writer:
                # Cria um arquivo Excel vazio se ele não existir
                if not os.path.exists(path_file):
                    Workbook().save(path_file)

                for year, data_by_year in data_by_year.items():
                    # Cria uma lista para armazenar os DataFrames de cada mês
                    dfs_years = []

                    for month_year, data in data_by_year.items():
                        # Adiciona o DataFrame do mês à lista
                        dfs_years.append(data)
                    # Concatena todos os DataFrames do ano
                    df_year = pd.concat([df_year, data], ignore_index=True)
                    # Salva o DataFrame do ano na aba correspondente
                    data.to_excel(writer, sheet_name=year, index=False)

        # with pd.ExcelWriter(f'{cpf }.xlsx') as writer:
        #     for month_year, data in data_by_month.items():
        #         data.to_excel(writer, sheet_name=month_year, index=False)

        return True

    except Exception as e:
        print(f"Erro ao realizar pesquisa: {e}")
        return False
    finally:
        driver.quit()
