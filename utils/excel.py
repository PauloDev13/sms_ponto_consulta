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

            # formats = {
            #     'numeric': workbook.add_format({'num_format': '#,##0'})
            # }
            #
            # worksheet.set_column('H:H', None, formats['numeric'])

            # cell_1 = 'K16'
            # cell_2 = 'H3'
            # cell_3 = 'H15'
            #
            # formula = f'=SUM({cell_2}:{cell_3})'

            # worksheet.write_array_formula('K16', f'{formula}')
            # worksheet.write_formula('K16', formula)
            # worksheet.write_formula('L16', 'K16')

            # workbook.set_calc_mode('manual')
            # workbook.set_calc_mode('auto')
