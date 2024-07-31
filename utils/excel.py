import pandas as pd

import os
from typing import Dict
from dotenv import load_dotenv

from utils import format_excel

load_dotenv()
file_path = os.getenv('PATH_FILE_BASE')

if not file_path:
    raise ValueError('O caminho para o arquivo do Excel não está definido no .env')


# Cria o arquivo Excel
def generate_excel_file(data_dic: Dict[int, pd.DataFrame], employee_name: str, cpf: str):
    file_name = os.path.join(file_path, f'{employee_name} - CPF_{cpf}.xlsx')
    # Usa o metódo ExcelWriter do Pandas para criar o arquivo
    # Excel usando a biblioteca xlsxwriter
    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
        # Itera sobre o dicionário (data_dic) extraindo o ano (year)
        # e o Dataframe com os dados dos meses do respectivo ano
        for year, df_year in data_dic.items():
            # Cria a planilha com abas para cada ano, começando
            # na linha índice 0do Dataframe, sem trazer os índices
            # das linha e o cabeçalho do Dataframe
            df_year.to_excel(writer, sheet_name=str(year), index=False, startrow=0, header=False)
            workbook = writer.book
            worksheet = writer.sheets[str(year)]

            # Chama a função (define_formats) do módulo (format_excel)
            #  passando a planilha do Excel (workbook) que será criada
            # e atribui a variável (formats)
            formats = format_excel.define_formats(workbook)

            # Chama a função (apply_formatting) do módulo (format_excel),
            # passando as planilhas (worksheet, o Dataframe (df_year) e a
            # variável (formats) definida anteriorment. Essa função aplica
            # as formatações nas planilhas que serão salvas no arquivo Excel.
            format_excel.apply_formatting(worksheet, df_year, formats)

# def generate_excel_file(dataframe: Dict[int, pd.DataFrame], employee_name: str, cpf: str):
#     file_name = os.path.join(file_path, f'{employee_name} - CPF_{cpf}.xlsx')
#     # with pd.ExcelWriter(fr'{file_path}\{employee_name} - CPF_{cpf}.xlsx', engine='xlsxwriter') as writer:
#
#     with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
#         # Itera sobre 'dataframe', que é um dicionário, extraindo
#         # os valores das chaves year e df_year (Dataframe) do dicionário,
#         for year, df_year in dataframe.items():
#             df_year.to_excel(writer, sheet_name=str(year), index=False, startrow=0, header=False)
#             workbook = writer.book
#             worksheet = writer.sheets[str(year)]
#
#             # DEFININDO FORMATAÇÕES QUE SERÃO APLICADAS EM CÉLULAS ESPECÍFICAS
#             header_format = workbook.add_format({
#                 'bold': True,
#                 'bg_color': '#B0C4DE',
#                 'align': 'center',
#             })
#
#             green_bold_format = workbook.add_format({
#                 'bold': True,
#                 'bg_color': 'green',
#                 'font_color': 'white',
#                 'align': 'center',
#             })
#
#             blue_bold_format = workbook.add_format({
#                 'bold': True,
#                 'bg_color': 'blue',
#                 'font_color': 'white',
#                 'align': 'center',
#             })
#
#             red_bold_format = workbook.add_format({
#                 'bold': True,
#                 'bg_color': 'red',
#                 'font_color': 'white',
#                 'align': 'center',
#             })
#
#             custom_format_1 = workbook.add_format({
#                 'top': 1,  # Borda superior fina
#                 'bottom': 1,  # Borda inferior fina
#                 'left': 1,  # Borda esquerda fina
#                 'bold': True,
#                 'bg_color': '#F0E68C',
#                 'align': 'center',
#                 'valign': 'top',
#             })
#
#             custom_format_2 = workbook.add_format({
#                 'top': 1,  # Borda superior fina
#                 'bottom': 1,  # Borda inferior fina
#                 'right': 1,  # Borda esquerda fina
#                 'text_wrap': True,
#                 'bold': True,
#                 'bg_color': '#F0E68C',
#                 'align': 'justify',
#                 'valign': 'top',
#             })
#
#             # Define larguras das colunas e o alinhamento centralizado em algumas
#             worksheet.set_column(0, 0, 25)
#             worksheet.set_column(1, 1, 20, workbook.add_format({'align': 'center'}))
#             worksheet.set_column(2, 2, 25)
#             worksheet.set_column(3, 6, 20, workbook.add_format({'align': 'center'}))
#             worksheet.set_column(7, 10, 5, workbook.add_format({'align': 'center'}))
#
#
#             # Aplica bordas em toda as linhas e colunas que contenham dados
#             worksheet.conditional_format(f'A1:J{len(df_year)}', {
#                 'type': 'no_blanks',
#                 'format': workbook.add_format({'border': 1})
#             })
#
#             # worksheet.write(row_index + 1, 7, sum_formula)
#                 # sum_formula = f'=SUM(H{len(df_year)}:H{row_index})'
#                 # print(f'FORMULA: {sum_formula}')
#
#             # Itera sobre o DataFrame
#             for row_index, row in df_year.iterrows():
#
#                 if row.iloc[0] == 'TOTAIS':
#                     worksheet.merge_range(
#                         row_index, 0, row_index, 6, row.iloc[0], workbook.add_format(
#                             {'align': 'right','bold': True, 'font_color': 'red'}))
#
#                 # Se a coluna 0 contiver as strings 'JUSTIFICATIVA' ou 'AVISO',
#                 # copia o conteúdo da linha e mescla as células das colunas 1 até 6
#                 # Se encontrar na coluna 0 (primeira coluna) as strings 'JUSTIFICATIVA' ou 'AVISO',
#                 # aplica formatação
#                 elif (row.iloc[0] == 'JUSTIFICATIVA') or (row.iloc[0] == 'AVISO'):
#                     worksheet.write(row_index, 0, row.iloc[0], custom_format_1)
#                     # Se o tamanho do conteúdo da célula na coluna 1 for > do que 150 caracteres,
#                     # aumenta a altura da linha para 50
#                     if 145 <= len(row.iloc[1]) <= 380:
#                         worksheet.set_row(row_index, 35)
#                     elif len(row.iloc[1]) >= 381:
#                         worksheet.set_row(row_index, 50)
#                     # Mescla as colunas a partir da coluna 1 até a última coluna
#                     # matendo o conteúdo da célula da coluna 1 nas células mescladas
#                     worksheet.merge_range(
#                         row_index, 1, row_index, 6, row.iloc[1], custom_format_2)
#
#                 # Itera sobre as colunas e linhas
#                 for col_index, value in enumerate(row):
#                     # Se a coluna for a primeira (índice 0) e o conteúdo da célula da primeira
#                     # linha começar com a string 'PONTO DIGITAL', formata os cabeçalhos
#                     # do início da planilha e entre os meses, aplicando borda e mesclando as células
#                     if col_index == 0 and value.startswith('PONTO DIGITAL'):
#                         worksheet.write(row_index, 0, row.iloc[0])
#                         worksheet.merge_range(
#                             row_index, 0, row_index, 10, value, header_format
#                         )
#
#                     # Se for a primeira coluna e o conteúdo da primeira célula da primeira
#                     # linha começar com a string 'NÃO HÁ REGISTRO', formata a linha e mescla
#                     # o intervalo de células com índices de 0 a 10
#                     if col_index == 0 and value.startswith('NÃO HÁ REGISTRO'):
#                         worksheet.write(row_index, 0, row.iloc[0])
#                         worksheet.set_row(row_index, 30)
#                         worksheet.merge_range(
#                             row_index, 0, row_index, 10, value, workbook.add_format({
#                                 'bg_color': '#FF8C00',
#                                 'align': 'center',
#                                 'valign': 'center',
#                                 'font_size': 20,
#                             })
#                         )
#
#                     # Formata com a cor verde as células da coluna horas trabalhadas
#                     # que contenham o valor >= a '12:00:00'
#                     if col_index == 4 and isinstance(value, str) and value >= '12:00:00':
#                         worksheet.write(row_index, col_index, value, green_bold_format)
#
#                     # Formata com a cor azul as células da coluna horas trabalhadas
#                     # que contenham o valor < '12:00:00'
#                     # excluindo as celulas vazias ou com a string '---'
#                     elif (col_index == 4 and isinstance(value, str)
#                           and value < '12:00:00' and value != '---' and value != ''):
#                         worksheet.write(row_index, col_index, value, blue_bold_format)
#
#                     # Se a célula da coluna 6 contiver a string 'APROVADO',
#                     # aplica formatação com a cor de fundo verde e cor da letra branca
#                     elif col_index == 6 and isinstance(value, str) and value == 'APROVADO':
#                         worksheet.write(row_index, col_index, value, green_bold_format)
#
#                     # Se o índice das colunas for maior que 6 e menor 11, aplica
#                     # formatação com bordas. Coloca bordas nas últimas 4 colunas
#                     elif 6 < col_index < 11:
#                         worksheet.write(row_index, col_index, value, workbook.add_format({'border': 1}))
#
#                 # Se o índice da coluna for < 11 e nela contiver a string 'DATA ENTRADA',
#                 # aplica formatação em toda a linha do cabeçalho das colunas
#                 for col in range(len(row)):
#                     if col < 11 and 'DATA ENTRADA' in row.values:
#                         worksheet.write(row_index, col, row.iloc[col], header_format)
