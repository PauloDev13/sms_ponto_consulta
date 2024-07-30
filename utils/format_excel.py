import os
from dotenv import load_dotenv

load_dotenv()
file_path = os.getenv('PATH_FILE_BASE')

if not file_path:
    raise ValueError("O caminho do arquivo base não está definido no .env")

# Fução que retorna um dicionário com a formatação
# para células individuais do arquivo Excel
def define_formats(workbook):
    formats = {
        'header': workbook.add_format({
            'bold': True,
            'bg_color': '#B0C4DE',
            'align': 'center',
        }),
        'green_bold': workbook.add_format({
            'bold': True,
            'bg_color': 'green',
            'font_color': 'white',
            'align': 'center',
        }),
        'blue_bold': workbook.add_format({
            'bold': True,
            'bg_color': 'blue',
            'font_color': 'white',
            'align': 'center',
        }),
        'red_bold': workbook.add_format({
            'bold': True,
            'bg_color': 'red',
            'font_color': 'white',
            'align': 'center',
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
        'no_blanks': workbook.add_format({'border': 1}),
        'warning': workbook.add_format({
            'bg_color': '#FF8C00',
            'align': 'center',
            'valign': 'center',
            'font_size': 20,
        }),
        'col_center': workbook.add_format({'align': 'center'}),
        'totais': workbook.add_format({
            'align': 'right',
            'bold': True,
            'font_color': 'red'
        })
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

    worksheet.conditional_format(f'A1:J{len(df_year)}', {
        'type': 'no_blanks',
        'format': formats['no_blanks']
    })

    for row_index, row in df_year.iterrows():
        if row.iloc[0] == 'TOTAIS':
            worksheet.merge_range(
                row_index, 0, row_index, 6, row.iloc[0], formats['totais'])

        elif row.iloc[0] in ['JUSTIFICATIVA', 'AVISO']:
            worksheet.write(row_index, 0, row.iloc[0], formats['custom_1'])
            if 145 <= len(row.iloc[1]) <= 380:
                worksheet.set_row(row_index, 35)
            elif len(row.iloc[1]) >= 381:
                worksheet.set_row(row_index, 50)
            worksheet.merge_range(
                row_index, 1, row_index, 6, row.iloc[1], formats['custom_2'])

        for col_index, value in enumerate(row):
            if col_index == 0 and value.startswith('PONTO DIGITAL'):
                worksheet.write(row_index, 0, row.iloc[0])
                worksheet.merge_range(
                    row_index, 0, row_index, 10, value, formats['header'])

            if col_index == 0 and value.startswith('NÃO HÁ REGISTRO'):
                worksheet.write(row_index, 0, row.iloc[0])
                worksheet.set_row(row_index, 30)
                worksheet.merge_range(
                    row_index, 0, row_index, 10, value, formats['warning'])

            if col_index == 4 and isinstance(value, str) and value >= '12:00:00':
                worksheet.write(row_index, col_index, value, formats['green_bold'])

            elif (col_index == 4 and isinstance(value, str)
                  and value < '12:00:00' and value not in ['---', '']):
                worksheet.write(row_index, col_index, value, formats['blue_bold'])

            elif col_index == 6 and isinstance(value, str) and value == 'APROVADO':
                worksheet.write(row_index, col_index, value, formats['green_bold'])

            elif 6 < col_index < 11:
                worksheet.write(row_index, col_index, value, formats['no_blanks'])

        for col in range(len(row)):
            if col < 11 and 'DATA ENTRADA' in row.values:
                worksheet.write(row_index, col, row.iloc[col], formats['header'])

# def generate_excel_file(dataframe: Dict[int, pd.DataFrame], employee_name: str, cpf: str):
#     file_name = os.path.join(file_path, f'{employee_name} - CPF_{cpf}.xlsx')
#
#     with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
#         for year, df_year in dataframe.items():
#             df_year.to_excel(writer, sheet_name=str(year), index=False, startrow=0, header=False)
#             workbook = writer.book
#             worksheet = writer.sheets[str(year)]
#
#             formats = define_formats(workbook)
#             apply_formatting(worksheet, df_year, formats)
