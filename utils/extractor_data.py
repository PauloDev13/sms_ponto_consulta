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
from services import authenticate


# Carrega o arquivo .env
load_dotenv()

# Define a localização como português do Brasil (pt_BR)
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Ler a URL base que vai montar a busca dos dados
url_data = os.getenv('URL_DATA')


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

                # Cria um dicionário com as colunas que serão criadas.
                # O conteúdo é de todas é vazio e terão o mesmo número
                # de linhas do Dataframe
                new_columns = {
                    'HT': [''] * df_table.shape[0],
                    'HJ': [''] * df_table.shape[0],
                    'ST': [''] * df_table.shape[0]
                }

                # Loop para criar as colunas no Dataframe
                for col_name, col_value in new_columns.items():
                    df_table[col_name] = col_value

                # Após criadas, as colunas vão receber os valore 1 ou vazio ('').
                # É aplicado no Dataframe (df_table) a função (columns_update) que
                # retorna esses valores
                df_table[['HT', 'HJ', 'ST']] = df_table.apply(utils.columns_update, axis=1)

                # Remove do dataframe (df_table) a coluna (EDITAR)
                del df_table['EDITAR']

                # Atribui a variável 'columns' o array com os nomes das colunas
                # do DataFrame (df_table)
                columns = df_table.columns

                # Atualiza o dataframe (df_table) substituindo o conteúdo das colunas
                # DATA SAÍDA, SAÍDA, TRABALHADA, HORA JUSTIFICADA e STATUS para uma string '---'
                # nas linhas onde a coluna DATA ENTRADA tem as palavra 'JUSTIFICATIVA' ou 'AVISO'
                # df_table.loc[
                #     df_table['DATA ENTRADA'].str.contains('JUSTIFICATIVA')
                #     | df_table['DATA ENTRADA'].str.contains('AVISO'),
                #     ['DATA SAÍDA', 'SAÍDA', 'TRABALHADA', 'HORA JUSTIFICADA', 'STATUS']
                # ] = '---'

                # Finaliza a limpeza dos dados no Dataframe (df_table
                # com o seguintes critérios:
                # 1 - São selecionadas as colunas TRABALHADA e HORA JUSTIFICADA que forem difentes de '---'
                # 2 - ou as colunas STATUS igual 'APROVADO' e DATA ENTRADA igual a 'JUSTIFICATIVA'
                df_result = df_table[
                    (df_table['TRABALHADA'] != '---')
                    | (df_table['HORA JUSTIFICADA'] != '---')
                    | (df_table['STATUS'] == 'APROVADO')
                    | (df_table['DATA ENTRADA'] == 'JUSTIFICATIVA')
                ]

                # Array de string com as colunas do Datafre (df_table) que serão verificadas
                columns_to_check = [
                    'DATA ENTRADA', 'ENTRADA', 'DATA SAÍDA', 'SAÍDA',
                    'TRABALHADA', 'HORA JUSTIFICADA', 'STATUS', 'HT', 'HJ', 'ST']


                # Verifica onde todas as colunas do dataframe estão vazias
                all_empty: bool = (
                        df_result[columns_to_check].isna().all(axis=1)
                        | (df_result[columns_to_check] == '').all(axis=1))

                # Cria uma nova linha com mensagem de alerta,
                # secrita na primeira céluna da coluna para os
                # meses que não retornam dados.
                message_row = (
                        [f'NÃO HÁ REGISTROS PARA O MÊS {month_name}/{year} - '
                         f'CONFIRMAR FÉRIAS OU LICENÇA'] +
                        [''] * (len(df_result.columns) - 1))

                # cria linha vazia
                empty_row = [''] * len(columns)


                # Se a variável 'all_empty' retornar verdadeiro
                if all_empty.empty:
                    # cria Dataframe (df_with_message) com a mensagem de alerta
                    # concatenando com o Dataframe (df_result)
                    df_with_message = pd.concat([pd.DataFrame(
                        [empty_row, message_row], columns=columns), df_result], ignore_index=True)
                else:
                    # Se não, atribui ao Datafram (df_with_message) o Dataframe (df_result) original.
                    df_with_message = df_result

                # Se o ano não existir no dicionário 'data_by_year',
                # adiciona o ano e processa dos dados para cada ano
                if year not in data_by_year:
                    # Define a mensagem inicial
                    header_message_1 = f'PONTO DIGITAL - {employee_name} - CPF: {cpf} - {month_name}/{year}'

                    # Cria DataFrame (data_by_year[year])
                    data_by_year[year] = pd.DataFrame([
                        [header_message_1]  + [''] * (len(columns) - 1), # Primeira linha com identificação
                        list(columns) # Segunda linha com o nome das colunas
                    ], columns=columns)

                    # Atualiza o Dataframe (data_by_year) mesclando com o Dataframe (df_with_message)
                    data_by_year[year] = pd.concat(
                        [data_by_year[year], df_with_message], ignore_index=True)
                else:
                    # Define mensagem de identificação exibida
                    # acima das colunas de cada mês
                    header_message_2 = f'PONTO DIGITAL - {employee_name} - CPF: {cpf} - {month_name}/{year}'

                    # Linha vazia (array [''], [''], [''], ['']...
                    empty_row = ['TOTAIS'] + [''] * (len(columns) -1)

                    # Cria Dataframe(df_employee_row) para exibir informações de cada mês
                    df_employee_row = pd.DataFrame([
                        empty_row, # Linha vazia no fim de cada mês
                        [header_message_2] + [''] * (len(columns) - 1), # Linha com identificação
                        list(columns) # Linha com os nomes das colunas (cabeçalho)
                    ], columns=columns)

                    # Atualiza o Dataframe (data_by_year) mesclando os Dataframes
                    # (df_employee_row e df_with_message)
                    data_by_year[year] = pd.concat(
                        [data_by_year[year], df_employee_row, df_with_message], ignore_index=True
                    )

            # Se ocorrer erro durante o processo de coleta e montagem de dados no DataFrame,
            # exibe mensagem de erro, espera 2 segundos e fecha a mensagem
            except TimeoutException as e:
                utils.default_msg(
                    f'Erro ao carregar dados para {month}/{year}', 'error')

                print(f'Erro ao carregar dados: {e}')

                authenticate.logout()

            # Incrementa em um mês a data inicial
            current_date += datetime.timedelta(days=32)
            # Modifica o dia da data inicial para o primeiro dia do mês
            current_date = current_date.replace(day=1)

        ########## FIM DO LAÇO WHILE ###########

            # Depuração: Imprime o conteúdo do dicionário data_by_year
            for year, df in data_by_year.items():
                print(f'Mês/Ano: {month_name}/{year}\nLinhas por ano: {len(df)}')

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


