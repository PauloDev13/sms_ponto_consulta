import pandas as pd

import os
from dotenv import load_dotenv

load_dotenv()
file_path = os.getenv('PATH_FILE_BASE')


def generate_excel_file(dataframe: any, employee_name: str, cpf: str):
    with pd.ExcelWriter(fr'{file_path}\{employee_name} - CPF_{cpf}.xlsx', engine='xlsxwriter') as writer:
        # Itera sobre 'dataframe', que é um dicionário, extraindo
        # os valores das chaves year e df_year (Dataframe) do dicionário,
        for year, df_year in dataframe.items():
            df_year.to_excel(writer, sheet_name=str(year), index=False, startrow=0, header=False)
            workbook = writer.book
            worksheet = writer.sheets[str(year)]

            # DEFININDO FORMATAÇÕES QUE SERÃO APLICADAS EM CÉLULAS ESPECÍFICAS
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#B0C4DE',
                'align': 'center',
            })

            green_bold_format = workbook.add_format({
                'bold': True,
                'bg_color': 'green',
                'font_color': 'white',
                'align': 'center',
            })

            blue_bold_format = workbook.add_format({
                'bold': True,
                'bg_color': 'blue',
                'font_color': 'white',
                'align': 'center',
            })

            red_bold_format = workbook.add_format({
                'bold': True,
                'bg_color': 'red',
                'font_color': 'white',
                'align': 'center',
            })

            custom_format_1 = workbook.add_format({
                'top': 1,  # Borda superior fina
                'bottom': 1,  # Borda inferior fina
                'left': 1,  # Borda esquerda fina
                'bold': True,
                'bg_color': '#F0E68C',
                'align': 'center',
                'valign': 'top',
            })

            custom_format_2 = workbook.add_format({
                'top': 1,  # Borda superior fina
                'bottom': 1,  # Borda inferior fina
                'right': 1,  # Borda esquerda fina
                'text_wrap': True,
                'bold': True,
                'bg_color': '#F0E68C',
                'align': 'justify',
                'valign': 'top',
            })

            # Define larguras das colunas e o alinhamento centralizado em algumas
            worksheet.set_column(0, 0, 25)
            worksheet.set_column(1, 1, 20, workbook.add_format({'align': 'center'}))
            worksheet.set_column(2, 2, 25)
            worksheet.set_column(3, 6, 20, workbook.add_format({'align': 'center'}))

            # Aplica bordas em toda as linhas e colunas que contenham dados
            worksheet.conditional_format(f'A1:G{len(df_year)}', {
                'type': 'no_blanks',
                'format': workbook.add_format({'border': 1})
            })

            # Itera sobre o DataFrame
            for row_index, row in df_year.iterrows():

                # Se a coluna 0 contiver as strings 'JUSTIFICATIVA' ou 'AVISO',
                # copia o conteúdo da linha e mescla as células das colunas 1 até 6
                # Se encontrar na coluna 0 (primeira coluna) as strings 'JUSTIFICATIVA' ou 'AVISO',
                # aplica formatação
                if (row.iloc[0] == 'JUSTIFICATIVA') or (row.iloc[0] == 'AVISO'):
                    worksheet.write(row_index, 0, row.iloc[0], custom_format_1)
                    # Se o tamanho do conteúdo da célula na coluna 1 for > do que 150 caracteres,
                    # aumenta a altura da linha para 50
                    if len(row.iloc[1]) >= 145 and len(row.iloc[1]) <= 380:
                        worksheet.set_row(row_index, 35)
                    elif len(row.iloc[1]) >= 381:
                        worksheet.set_row(row_index, 50)
                    # Mescla as colunas a partir da coluna 1 até a última coluna
                    # matendo o conteúdo da célula da coluna 1 nas células mescladas
                    worksheet.merge_range(
                        row_index, 1, row_index, 6, row.iloc[1], custom_format_2)

                # Itera sobre as colunas e linhas
                for col_index, value in enumerate(row):
                    # Se a coluna for a primeira (índice 0) e o conteúdo da célula da primeira
                    # linha começar com a string 'PONTO DIGITAL', Formata os cabeçalhos
                    # do início da planilha e entre os meses, aplicando borda e mesclando as células
                    if col_index == 0 and value.startswith('PONTO DIGITAL'):
                        worksheet.write(row_index, 0, row.iloc[0])
                        worksheet.merge_range(
                            row_index, 0, row_index, 6, value, header_format
                        )

                    # Formata com a cor verde as células da coluna horas trabalhadas
                    # que contenham o valor >= a '12:00:00'
                    if col_index == 4 and isinstance(value, str) and value >= '12:00:00':
                        worksheet.write(row_index, col_index, value, green_bold_format)

                    # Formata com a cor azul as células da coluna horas trabalhadas
                    # que contenham o valor < '12:00:00'
                    # excluindo as celulas vazias ou com a string '---'
                    elif (col_index == 4 and isinstance(value, str)
                          and value < '12:00:00' and value != '---' and value != ''):
                        worksheet.write(row_index, col_index, value, blue_bold_format)

                    # Se a célula da coluna 6 contiver a string 'APROVADO',
                    # aplica formatação com a cor de fundo verde e cor da letra branca
                    elif col_index == 6 and isinstance(value, str) and value == 'APROVADO':
                        worksheet.write(row_index, col_index, value, green_bold_format)

                # Se o índice da coluna for < 7 e nela contiver a string 'DATA ENTRADA',
                # aplica formatação em toda a linha do cabeçalho das colunas
                for col in range(len(row)):
                    if col < 7 and 'DATA ENTRADA' in row.values:
                        worksheet.write(row_index, col, row.iloc[col], header_format)
