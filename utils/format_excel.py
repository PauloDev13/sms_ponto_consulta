import os
import xlsxwriter
from dotenv import load_dotenv

load_dotenv()
file_path = os.getenv('PATH_FILE_BASE')
password_workbook = os.getenv('PASSWORD')

if not file_path or not password_workbook:
    raise ValueError("O caminho do arquivo base não está definido no .env")

# Fução que retorna um dicionário com a formatação
# para células individuais do arquivo Excel
def define_formats(workbook):
    formats = {
        'header': workbook.add_format({
            'bold': True,
            'bg_color': '#B0C4DE',
            'align': 'center',
            'border': 1,
        }),
        'green_bold': workbook.add_format({
            'bold': True,
            'bg_color': 'green',
            'font_color': 'white',
            'align': 'center',
            'border': 1,
        }),
        'blue_bold': workbook.add_format({
            'bold': True,
            'bg_color': 'blue',
            'font_color': 'white',
            'align': 'center',
            'border': 1,
        }),
        'red_bold': workbook.add_format({
            'bold': True,
            'bg_color': 'red',
            'font_color': 'white',
            'align': 'center',
            'border': 1,
        }),
        'custom_1': workbook.add_format({
            'top': 1,
            'bottom': 1,
            'left': 1,
            'bold': True,
            'bg_color': '#F0E68C',
            'align': 'center',
            'valign': 'top',
        }),
        'custom_2': workbook.add_format({
            'top': 1,
            'bottom': 1,
            'right': 1,
            'text_wrap': True,
            'bold': True,
            'bg_color': '#F0E68C',
            'align': 'justify',
            'valign': 'top',
        }),
        'all_borders': workbook.add_format({
            'border': 1,
            'bg_color': '#F0F8FF',
        }),
        'warning': workbook.add_format({
            'bg_color': '#FF8C00',
            'align': 'center',
            'valign': 'center',
            'font_size': 20,
            'border': 1,
        }),
        'col_center': workbook.add_format({'align': 'center'}),
        'results': workbook.add_format({
            'bold': True,
            'align': 'center',
            'font_color': 'red',
            'border': 1,
        }),
        'col_total': workbook.add_format({
            'bold': True,
            'align': 'right',
            'font_color': 'red',
            'border': 1,
        }),
        'single_border': workbook.add_format({
            'border': 1,
            'align': 'center',
        }),
        'cell_unblocked': workbook.add_format({'locked': False}),
    }
    return formats


# Função que implementa condicionais e formatação
# (usando a função define_formats) em células individuais do arquivo Excel
def apply_formatting(worksheet, df_year, formats):
    worksheet.set_column(0, 0, 25)
    worksheet.set_column(1, 1, 20, formats['col_center'])
    worksheet.set_column(2, 2, 25)
    worksheet.set_column(3, 6, 20, formats['col_center'])
    worksheet.set_column(7, 10, 5, formats['col_center'])

    last_header_index = -1

    # Itera sobre as linhas do Dataframe (df_year) criando
    #  uma (Series) com os índices e o conteúdo de cada linha
    for row_index, row in df_year.iterrows():


        if row.iloc[0] == 'DATA ENTRADA':
            # Se o conteúdo da coluna índice 0 for igual a string 'DATA ENTRADA',
            # atribui a variável (last_header_index) o valor do índice da
            # última linha de cada mês
            last_header_index = row_index


        elif row.iloc[1] and 0 < len(row.iloc[1]) <= 8:
            worksheet.write(row_index, 1, row.iloc[1], formats['single_border'])


        elif row.iloc[0] not in ['JUSTIFICATIVA', 'AVISO']:
            worksheet.write(row_index, 0, row.iloc[0], formats['single_border'])

        # Se na coluna índice 0 o conteúdo da célula form igual a
        # 'JUSTIFICATIVA' ou 'AVISO', aplica formatação
        elif row.iloc[0] in ['JUSTIFICATIVA', 'AVISO']:
            worksheet.write(row_index, 0, row.iloc[0], formats['custom_1'])
            # Se na coluna índice 1 o conteúdo da célula for >= a 145
            # e <= 380 caracteres, aumenta a altura da linha para 30
            if 145 <= len(row.iloc[1]) <= 380:
                worksheet.set_row(row_index, 35)
            # Se na mesma coluna o conteúdo da célula for,
            #  >= a 381, aumenta a altura da linha para 50
            elif len(row.iloc[1]) >= 381:
                worksheet.set_row(row_index, 50)
            # Mescla as células da linha entre as colunas com
            # índices 1 a 6 e aplica formatação
            worksheet.merge_range(
                row_index, 1, row_index, 6, row.iloc[1], formats['custom_2'])

        # Itera sobre as linhas criando uma (Series) que
        # contém o índice e os valores em cada coluna por linha
        for col_index, value in enumerate(row):
            # Se o índice da coluna for == a 0 e o valor da célula começar
            #  com a string 'PONTO DIGITAL', mescla as células de toda a linha
            if col_index == 0 and value.startswith('PONTO DIGITAL'):
                worksheet.merge_range(
                    row_index, 0, row_index, 10, value, formats['header'])

            # Se a string 'DATA ENTRADA' estiver em alguma
            #  célula da coluna, aplica formatação
            elif 'DATA ENTRADA' in row.values:
                worksheet.write(row_index, col_index, row.iloc[col_index], formats['header'])

            # Se o índice da coluna for == a 0 e o valor da célula começar
            # com a string 'NÃO HÁ REGISTRO', mescla as células de toda a linha
            elif col_index == 0 and value.startswith('NÃO HÁ REGISTRO'):
                worksheet.set_row(row_index, 30)
                worksheet.merge_range(
                    row_index, 0, row_index, 10, value, formats['warning'])

            elif 1 < col_index < 4:
                worksheet.write(row_index, col_index, value, formats['single_border'])

            # Se o índice da coluna for == a 4 e o valor da célula for >=
            #  a '12:00:00', aplica formatação background verde e fonte branca.
            elif col_index == 4 and isinstance(value, str) and value >= '12:00:00':
                worksheet.write(row_index, col_index, value, formats['green_bold'])

            # Se na coluna índice 4 o valor da célula for < '12:00:00'
            # e != da string ('---') ou vazia (''), aplica formatação
            # background azul e fonte branca.
            elif (col_index == 4 and isinstance(value, str)
                  and value < '12:00:00' and value not in ['---', '']):
                worksheet.write(row_index, col_index, value, formats['blue_bold'])

            # Se a coluna é índice 6, aplica formatação
            # insere bordas em todas as células da coluna
            elif col_index == 5:
                worksheet.write(row_index, col_index, value, formats['single_border'])

            # Se na coluna índice 6 o valor da célula for == a
            # 'APROVADO', aplica formatação background verde e fonte branca.
            elif col_index == 6 and value == 'APROVADO':
                worksheet.write(row_index, col_index, value, formats['green_bold'])

            # Se na coluna índice 6 o valor da célula for == 'REPROVADO' ou
            # 'ESPERA', aplica formatação background vermelho e fonte branca.
            elif col_index == 6 and value == 'REPROVADO' or value == 'ESPERA':
                worksheet.write(row_index, col_index, value, formats['red_bold'])

            # Se a coluna é índice 6, aplica formatação
            # insere bordas em todas as células da coluna
            elif col_index == 6:
                worksheet.write(row_index, col_index, value, formats['single_border'])

            # Se o índice da coluna for > 6 e < 11, aplica a formação que
            # insere bordas em todas as células do intervalo de colunas
            elif col_index > 6:
                worksheet.conditional_format(f'H{row_index}:K{row_index}', {
                    'type': 'cell',
                    'criteria': '>=',
                    'value': 0,
                    'format': formats['all_borders']
                })


            elif value == 'TOTAIS':
                # Se nas colunas existir uma célula com valor igual a 'TOTAIS',
                # mescla todas as células da linha e aplica formatação
                worksheet.merge_range(
                    row_index, 0, row_index, 6, row.iloc[0], formats['col_total'])

                merged_cells = 7
                formula_col = merged_cells

                # start_row = last_header_index + 1 if last_header_index >= 0 else 1
                if last_header_index >= 0:
                    start_row = last_header_index + 1
                else:
                    start_row = 1

                end_row = row_index - 1

                if start_row <= end_row:
                    start_cell = xlsxwriter.utility.xl_rowcol_to_cell(start_row, formula_col)
                    end_cell = xlsxwriter.utility.xl_rowcol_to_cell(end_row, formula_col)

                    for index in range(0, 4):
                        start_cell = xlsxwriter.utility.xl_rowcol_to_cell(start_row, formula_col + index)
                        end_cell = xlsxwriter.utility.xl_rowcol_to_cell(end_row, formula_col + index)

                        formula = f'=SUM({start_cell}:{end_cell})'

                        worksheet.write_array_formula(
                            end_row + 1,
                            formula_col + index,
                            end_row + 1,
                            formula_col + index,
                            formula,
                            formats['results']
                        )

                else:
                    worksheet.write(row_index, formula_col, 0)


        # worksheet.protect(password_workbook)

        # Itera sobre o número de colunas por linha extraindo o índice de cada coluna
        # for col in range(len(row)):
            # Se o índice da coluna for menor que 11 e a string 'DATA ENTRADA'
            # estiver em alguma célula da linha, aplica formatação
            # if col < 11 and 'DATA ENTRADA' in row.values:
            #     worksheet.write(row_index, col, row.iloc[col], formats['header'])
