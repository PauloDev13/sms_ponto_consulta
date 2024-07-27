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

from utils import utils, excel


# Carrega o arquivo .env
load_dotenv()

# Define a localização como português do Brasil (pt_BR)
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Ler a URL base que vai montar a busca dos dados
url_data = os.getenv('URL_DATA')
# file_path = os.getenv('PATH_FILE_BASE')


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
                # df_table.loc[
                #     df_table['DATA ENTRADA'].str.contains('JUSTIFICATIVA')
                #     | df_table['DATA ENTRADA'].str.contains('AVISO'),
                #     ['DATA SAÍDA', 'SAÍDA', 'TRABALHADA', 'HORA JUSTIFICADA', 'STATUS']
                # ] = '---'

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

                ###########################################################################
                columns_to_check = [
                    'DATA ENTRADA', 'ENTRADA', 'DATA SAÍDA', 'SAÍDA',
                    'TRABALHADA', 'HORA JUSTIFICADA', 'STATUS']

                # Verifica onde todas as colunas estão vazias
                all_empty = df_result[columns_to_check].isna().all(axis=1) | (df_result[columns_to_check] == '').all(axis=1)
                print(f'ENTROU AQUI {all_empty}')

                # Cria uma nova linha com a mensagem "SEM DADOS PARA ESTE MÊS"
                message_row = ['SEM DADOS PARA ESTE MÊS. Veifique se o servidor está de FÉRIAS OU DE LICENÇA'] * len(df_result.columns)

                if all_empty.empty:
                    # Adiciona a linha de mensagem
                    df_with_message = pd.concat([pd.DataFrame([message_row], columns=df_result.columns), df_result],
                                                ignore_index=True)

                else:
                    df_with_message = df_result

                ###########################################################################

                # Se o ano não existir no dicionário 'data_by_year', adiciona-o
                if year not in data_by_year:
                    # Cria um DataFrame vazio somente com a linha do cabeçalho
                    data_by_year[year] = pd.DataFrame(columns=df_with_message.columns)

                    # Cria uma string com a frase 'DETALHAMENTO DO PONTO DIGITAL'
                    # concatenada com as variáveis 'employee_name', 'cpf', 'month_name' e 'year'
                    # que vai ser impressa no topo do arquivo Excel
                    data_by_year[year].loc[0, data_by_year[year].columns[0]] = (
                        f'PONTO DIGITAL - {employee_name} - CPF: {cpf} - '
                        f'{month_name}/{year}')

                    # Cria uma linha com os dados do cabeçalho abaixo da frase
                    header_row = pd.DataFrame([df_with_message.columns], columns=df_with_message.columns)


                    # Concatena os valores já existentes no Dataframe, para que o mesmo
                    # contenha as novas linhas criadas
                    data_by_year[year] = pd.concat(
                        [data_by_year[year], header_row, df_with_message], ignore_index=True)
                else:
                    # Cria uma linha vazia no início de cada mês
                    empty_row = pd.DataFrame([[''] * len(df_with_message.columns)], columns=df_with_message.columns)

                    # Cria uma string com a frase DETALHAMENTO DO PONTO DIGITAL concatenada
                    # com as variáveis 'employee_name', 'cpf', 'month_name' e 'year'
                    # que vai ser impressa no início de cada mês
                    employee_row: str = (f'PONTO DIGITAL - {employee_name} - CPF: {cpf} - '
                                    f'{month_name}/{year}')

                    # Cria uma linha para exibir a string 'employee_row'
                    data_employee_row = pd.DataFrame([
                        [employee_row] + [''] * (df_with_message.shape[1] - 1)], columns=df_with_message.columns)

                    # Concatena os valores já existentes no Dataframe, para que o mesmo
                    # contenha as novas linhas criadas
                    data_by_year[year] = pd.concat(
                        [data_by_year[year],
                         empty_row, data_employee_row, header_row, df_with_message],
                        ignore_index=True
                    )

            # Se ocorrer erro durante o processo de coleta e montagem de dados no DataFrame,
            # exibe mensagem de erro, espera 2 segundos e fecha a mensagem
            except TimeoutException:
                utils.default_msg(
                    f'Erro ao montar dados carregados da tabela para {month}/{year}', 'error')

            current_date += datetime.timedelta(days=32)
            current_date = current_date.replace(day=1)
        ########## FIM DO LAÇO WHILE ###########

            # Depuração: Imprime o conteúdo do dicionário data_by_year
            for year, df in data_by_year.items():
                print(f'Ano: {year}\nLinhas por ano: {len(df)}')


        # Chama a função que cria, formata e salva o arquivo Excel
        excel.generate_excel_file(data_by_year, employee_name, cpf)

        # Retorna verdadeiro se toda operação foi realizada com sucesso
        return True

    # Se ocorrerem erros, exibe mensagem
    except Exception as e:
        utils.default_msg('Erro ao gerar arquivo!', 'error')
        print(f'Erro ao gerar arquivo: {e}')

        # Retorna falso em caso de erro
        return False


