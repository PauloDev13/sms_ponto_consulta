from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

import pandas as pd
from bs4 import BeautifulSoup

import os
import datetime
import locale
import calendar
from io import StringIO
from dotenv import load_dotenv

import numpy as np

from utils import utils


# Carrega o arquivo .env
load_dotenv()

# Define a localização como português do Brasil (pt_BR)
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

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
        # são atribuídos as variáves 'month' e 'year' os valores
        # do mês e ano extraídos das datas informadas
        while current_date <= end_date:
            month = current_date.month
            year = current_date.year

            # Usa a biblioteca 'calendar' para extrair o nome do mês e
            # a biblioteca 'locale' para tradução em português
            month_name = calendar.month_name[month].upper()

            # Monta e atribui a variável 'table' a URL com os query params
            # da pesquisa e abre no navegador
            url_search = f'{url_data}?cpf={cpf}&mes={month}&ano={year}'
            driver.get(url_search)

            try:
                # Verifica se o elemento HTML contém a tag 'span/font[1]'
                WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[4]/div/span/font[1]")
                    )
                )
                # Procura e atribui a variável 'employee_name' o conteúdo da tag 'span/font[1]'
                employee_name = driver.find_element(
                    By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[4]/div/span/font[1]"
                ).text
                # Verifica se o elemento HTML contém uma tag table
                table = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, "//*[@id='mesatual']/table"))
                )

                # Utiliza a biblioteca BeautifulSoup para pegar o HTML da table
                # e atribui o resultado à variável 'soup' como uma string
                soup_table = BeautifulSoup(table.get_attribute("outerHTML"), 'html.parser')

                # Utiliza a biblioteca Pandas para montar DataFrame com todos os dados
                # da primeira table encontrada no HTML
                df_table = pd.read_html(StringIO(str(soup_table)))[0]

                # Remove do dataframe (df_table) a coluna (EDITAR)
                del df_table['EDITAR']

                # Atualiza o dataframe (df_table) substituindo o conteúdo das colunas
                # DATA SAÍDA, SAÍDA, TRABALHADA, HORA JUSTIFICADA e STATUS para uma string '---'
                # nas linhas onde a coluna DATA ENTRADA tem as palavra 'JUSTIFICATIVA' ou 'AVISO'
                df_table.loc[
                    df_table['DATA ENTRADA'].str.contains('JUSTIFICATIVA')
                    | df_table['DATA ENTRADA'].str.contains('AVISO'),
                    ['DATA SAÍDA', 'SAÍDA', 'TRABALHADA', 'HORA JUSTIFICADA', 'STATUS']
                ] = '---'

                # Finaliza a limpeza dos dados criando um novo dataframe (df_result)
                # com o seguintes critérios:
                # 1 - Colunas TRABALHADA e HORA JUSTIFICADA difentes de '---'
                # 2 - Colunas STATUS igual 'APROVADO' e DATA ENTRADA igual a 'JUSTIFICATIVA'
                df_result = df_table[
                    (df_table['TRABALHADA'] != '---')
                    | (df_table['HORA JUSTIFICADA'] != '---')
                    | (df_table['STATUS'] == 'APROVADO')
                    | (df_table['DATA ENTRADA'] == 'JUSTIFICATIVA')
                ]

                # Se o ano não existir no dicionário 'data_by_year', adiciona-o
                if year not in data_by_year:
                    # Cria um DataFrame vazio somente com a linha do cabeçalho
                    data_by_year[year] = pd.DataFrame(columns=df_result.columns)

                    # Cria uma string com a frase 'DETALHAMENTO DO PONTO DIGITAL'
                    # concatenada com as variáveis 'employee_name', 'cpf', 'month_name' e 'year'
                    # que vai ser impressa no topo do arquivo Excel
                    data_by_year[year].loc[0, data_by_year[year].columns[0]] = (
                        f'PONTO DIGITAL - {employee_name} - CPF: {cpf} - '
                        f'{month_name}/{year}')

                    # Cria uma linha com os dados do cabeçalho abaixo da frase
                    header_row = pd.DataFrame([df_result.columns], columns=df_result.columns)


                    # Concatena os valores já existentes no Dataframe, para que o mesmo
                    # contenha as novas linhas criadas
                    data_by_year[year] = pd.concat(
                        [data_by_year[year], header_row, df_result], ignore_index=True)
                else:
                    # Cria uma linha vazia no início de cada mês
                    empty_row = pd.DataFrame([[''] * len(df_result.columns)], columns=df_result.columns)

                    # Cria uma string com a frase DETALHAMENTO DO PONTO DIGITAL concatenada
                    # com as variáveis 'employee_name', 'cpf', 'month_name' e 'year'
                    # que vai ser impressa no início de cada mês
                    employee_row = (f'PONTO DIGITAL - {employee_name} - CPF: {cpf} - '
                                    f'{month_name}/{year}')

                    # Cria uma linha para exibir a string 'employee_row'
                    data_employee_row = pd.DataFrame([
                        [employee_row] + [''] * (df_result.shape[1] - 1)], columns=df_result.columns)

                    # Concatena os valores já existentes no Dataframe, para que o mesmo
                    # contenha as novas linhas criadas
                    data_by_year[year] = pd.concat(
                        [data_by_year[year], empty_row, data_employee_row, header_row, df_result], ignore_index=True)

            # Se ocorrer erro durante o processo de coleta e montagem de dados no DataFrame,
            # exibe mensagem de erro, espera 2 segundos e fecha a mensagem
            except TimeoutException:
                utils.default_msg(
                    f'Erro ao montar dados carregados da tabela para {month}/{year}', 'error')

            current_date += datetime.timedelta(days=32)
            current_date = current_date.replace(day=1)
        # FIM DO LAÇO WHILE

        # Depuração: Imprime o conteúdo do dicionário data_by_year
        for year, df in data_by_year.items():
            print(f"Ano: {year}, Número de Linhas: {len(df)}")

        # Itera sobre as chaves (anos) e valores (DataFrames) do dicionário,
        # cria o arquivo excel com os dados agrupados por ano em cada aba e salva na pasta BOT
        with pd.ExcelWriter(fr'{file_path}\{employee_name} - CPF_{cpf}.xlsx', engine='xlsxwriter') as writer:
            for year, df_year in data_by_year.items():
                df_year.to_excel(writer, sheet_name=str(year), index=False, startrow=0, header=False)
                workbook = writer.book
                worksheet = writer.sheets[str(year)]

                # Definindo as formatações que serão aplicadas nas linhas e colunas
                header_format = workbook.add_format({
                    'bold': True,
                    'bg_color': '#B0C4DE',
                    'align': 'center',
                    'border': 1,
                    'border_color': 'black'
                })

                row_format = workbook.add_format({
                        'top': 1,  # Borda superior fina
                        'bottom': 1,  # Borda inferior fina
                        'right': 1,  # Borda esquerda fina
                        'border_color': 'black',
                        'bold': True,
                        'bg_color': '#F0E68C',
                        'align': 'center'
                })

                col_format = workbook.add_format({'align': 'center'})

                # Formata bordas em todas as linhas e colunas
                border_format = workbook.add_format({
                    'border': 1,
                    'border_color': 'black',
                    'align': 'center'
                })

                green_bold_format = workbook.add_format({
                    'bold': True,
                    'font_color': 'green',
                    'align': 'center',
                    'border': 1,
                    'border_color': 'black'
                })

                blue_bold_format = workbook.add_format({
                    'bold': True,
                    'font_color': 'blue',
                    'align': 'center',
                    'border': 1,
                    'border_color': 'black'
                })

                # Definindo um formato com bordas específicas
                format_borders = workbook.add_format({
                    'top': 1,  # Borda superior fina
                    'bottom': 1,  # Borda inferior fina
                    'left': 1,  # Borda esquerda fina
                    'border_color': 'black',
                    'bold': True,
                    'bg_color': '#F0E68C',
                    'align': 'center'
                })

                # Definindo larguras das colunas
                worksheet.set_column(0, 0, 25)
                worksheet.set_column(1, 1, 20)
                worksheet.set_column(2, 2, 25)
                worksheet.set_column(3, 6, 20)

                # Itera sobre as linhas do DataFrame para encontrar as linhas
                # com a string 'DATA ENTRADA' e aplica a formatação
                for row_index, row in df_year.iterrows():
                    for col_index, value in enumerate(row):

                        # Formata com a cor verde as horas trabalhadas >= a 12:00:00
                        if col_index == 4 and isinstance(value, str) and value >= '12:00:00':
                            worksheet.write(row_index, col_index, value, green_bold_format)

                        # Formata com a cor azul as horas trabalhadas < a 12:00:00
                        elif col_index == 4 and isinstance(value, str) and value < '12:00:00':
                            worksheet.write(row_index, col_index, value, blue_bold_format)

                        elif col_index == 6 and isinstance(value, str) and value == 'APROVADO':
                            worksheet.write(row_index, col_index, value, green_bold_format)

                        # Aplica borda em todas as linhas com índice != 0
                        elif row_index != 0:
                            worksheet.write(row_index, col_index, value, border_format)

                    # Mescla as celulas da linha com índice 0 das colunas 0 até a 6
                    if row_index == 0:
                        worksheet.merge_range(
                            0, 0, 0, 6, row.iloc[0], header_format
                        )

                    # Se a coluna 0 contiver as strings 'JUSTIFICATIVA' ou 'AVISO',
                    # copia o conteúdo da linha e mescla as células das colunas 1 até 6
                    if (row.iloc[0] == 'JUSTIFICATIVA') or (row.iloc[0] == 'AVISO'):
                        worksheet.write(row_index, 0, row.iloc[0], format_borders)

                        worksheet.merge_range(
                            row_index, 1, row_index, 6, row.iloc[1], row_format
                        )

                    # Se a coluna contém o nome do servidor, mescla a linha das colunas 0 a 6
                    if (row.iloc[0] == employee_row):
                        worksheet.merge_range(
                            row_index, 0, row_index, 6, row.iloc[0], header_format
                        )

                    # Se o índice da coluna for < 7 e contiver a string 'DATA ENTRADA',
                    # copia o conteúdo das celulas linha em todas as colunas
                    for col in range(len(row)):
                        if col < 7 and 'DATA ENTRADA' in row.values:
                            worksheet.write(row_index, col, row.iloc[col], header_format)

        # Retorna verdadeiro se toda operação foi realizada com sucesso
        return True

    # Se ocorrerem erros, exibe mensagem
    except Exception as e:
        utils.default_msg('Erro ao gerar arquivo!', 'error')
        print(f'Erro ao gerar arquivo: {e}')

        # Retorna falso em caso de erro
        return False


