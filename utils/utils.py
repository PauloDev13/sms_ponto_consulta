import streamlit as st

import pandas as pd

import os
from time import sleep
from dotenv import load_dotenv

from services import authenticate
from utils import extractor_data

load_dotenv()
file_path = os.getenv('PATH_FILE_BASE')


# Função que insere '.' e '-' no número do CPF, caso tenha sido
# informado somente números.
def format_cpf(cpf: str) -> str:
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'


# Instancia mensagem de alerta de acordo com os parâmetro informados
def default_msg(msg: str, icon_msg: str):
    try:
        match icon_msg:
            case 'success':
                toast_msg = st.success(msg, icon='✅')
                # toast_msg = st.toast(msg, icon='✅')
            case 'warning':
                toast_msg = st.warning(msg, icon='⚠️')
                # toast_msg = st.toast(msg, icon='⚠️')
            case 'info':
                toast_msg = st.info(msg, icon='ℹ️')
                # toast_msg = st.toast(msg, icon='ℹ️')
            case _:
                toast_msg = st.error(msg, icon='🚨')
                # toast_msg = st.toast(msg, icon='🚨')
        sleep(3)
        toast_msg.empty()
        return toast_msg

    except Exception as ex:
        default_msg('Erro na messege', 'error')
        print(f'Erro stacktrace: {ex}')

# Função para validar as datas
def validate_dates(date_start, date_end):
    try:
        if not date_start:
            default_msg('A data de início é obrigatória.!', 'info')
            return False
        if not date_end:
            default_msg('A data final é obrigatória!', 'info')
            return False
        if date_start > date_end:
            default_msg('A data de início não pode ser posterior à data final!', 'info')
            return False
        return True
    except Exception as ex:
        default_msg('Erro ao validar datas', 'error')
        print(f'Erro stacktrace: {ex}')


# Função para validar o CPF
def validate_cpf(cpf):
    try:
        # Remove caracteres não numéricos
        # cpf_2 = ''.join(filter(str.isdigit, cpf))
        # st.write(cpf)

        if not cpf:
            default_msg('O CPF é obrigatório!', 'info')
            return False

        if not cpf.isdigit():
            default_msg('O CPF deve conter somente números!', 'info')
            return False

        if len(cpf) != 11:
            default_msg('CPF inválido', 'info')
            return False

        if cpf == cpf[0] * 11:
            default_msg('CPF inválido', 'info')
            return False

        # Calcula o primeiro dígito verificador
        sum_ = sum(int(cpf[i]) * (10 - i) for i in range(9))
        first_digit = (sum_ * 10 % 11) % 10

        # Calcula o segundo dígito verificador
        sum_ = sum(int(cpf[i]) * (11 - i) for i in range(10))
        second_digit = (sum_ * 10 % 11) % 10

        # Verifica se os dígitos calculados são iguais aos dígitos verificadores do CPF
        if first_digit == int(cpf[9]) and second_digit == int(cpf[10]):
            return True
        else:
            default_msg('CPF inválido', 'info')
            return False
    except Exception as ex:
        default_msg('Erro ao validar CPF', 'error')
        print(f'Erro stacktrace: {ex}')


# Limpa os campos do formulário no Session State
def fields_clear():
    st.session_state['cpf'] = ''
    st.session_state['date_start'] = None
    st.session_state['date_end'] = None


# Função de callback
def form_callback():
    # Pega os valores digitados no formulário vindos no Session State
    cpf_input = st.session_state['cpf']
    date_start = st.session_state['date_start']
    date_end = st.session_state['date_end']

    # Valida o CPF
    cpf_valid = validate_cpf(cpf_input)

    # Se o CPF for válido e tiver 11 números, formata aplicando uma máscara
    if cpf_valid:
        cpf_input = format_cpf(cpf_input)
        # if len(cpf_input) == 11:

        # Valida as datas
        dates_valid = validate_dates(date_start, date_end)

    # Se datas e CPF forem válidas, extrai os meses e anos de inícil e final
    if cpf_valid and dates_valid:
        month_start = date_start.month
        year_start = date_start.year
        month_end = date_end.month
        year_end = date_end.year

        # Verifica se existe uma sessão no Streamlit para o usuário logado
        # Se NÃO, chama a função 'login' do módulo 'authenticate' que retorna uma instância do navegador
        # Armazena a instância retornada numa sessão do Streamlit
        if 'driver' not in st.session_state:
            if driver := authenticate.login():
                st.session_state.driver = driver
                st.session_state['driver'] = driver
                driver.minimize_window()

                # Exibe um spinner até que a funçao 'data_fetch'
                # do módulo 'extrator_data' conclua a execução
                with st.spinner('Gerando arquivo...'):
                    result = extractor_data.data_fetch(
                        cpf_input, month_start, year_start, month_end, year_end, st.session_state.driver
                    )

                # Se a função retornar TRUE, o arquivo foi gerado com sucesso,
                # limpa os campos do formulário e exibe mensagem de sucesso
                if result:
                    default_msg('Arquivo criado com sucesso!', 'success')

        else:
            # Se já existir uma sessão aberta no Stremlit, repete o processo de geração do arquivo
            with st.spinner('Gerando arquivo...'):
                result = extractor_data.data_fetch(
                    cpf_input, month_start, year_start, month_end, year_end, st.session_state.driver
                )

            # Se a função retornar TRUE, o arquivo foi gerado com sucesso,
            # limpa os campos do formulário e exibe mensagem de sucesso
            if result:
                default_msg('Arquivo criado com sucesso!', 'success')


# def generate_excel_file(dataframe: any, employee_name: str, cpf: str):
#
#     with pd.ExcelWriter(fr'{file_path}\{employee_name} - CPF_{cpf}.xlsx', engine='xlsxwriter') as writer:
#
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
#                 'valign': 'center',
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
#                 'valign': 'center',
#             })
#
#             # Define larguras das colunas e o alinhamento centralizado em algumas
#             worksheet.set_column(0, 0, 25)
#             worksheet.set_column(1, 1, 20, workbook.add_format({'align': 'center'}))
#             worksheet.set_column(2, 2, 25)
#             worksheet.set_column(3, 6, 20, workbook.add_format({'align': 'center'}))
#
#             # Aplica bordas em toda as linhas e colunas que contenham dados
#             worksheet.conditional_format(f'A1:G{len(df_year)}', {
#                 'type': 'no_blanks',
#                 'format': workbook.add_format({'border': 1})
#             })
#
#             # Itera sobre o DataFrame
#             for row_index, row in df_year.iterrows():
#                 # if row.iloc[0] != 'DATA ENTRADA':
#                 #
#                 #     cell_trab = f'E{row_index + 1}'
#                 #
#                 #     worksheet.conditional_format(cell_trab, {
#                 #         'type': 'formula',
#                 #         'criteria': f'=${cell_trab}>="12:00:00"',
#                 #         'format': green_bold_format
#                 #     })
#                 #
#                 #     worksheet.conditional_format(cell_trab, {
#                 #         'type': 'formula',
#                 #         'criteria':
#                 #             f'=NOT(OR(${cell_trab}>="12:00:00", ${cell_trab}="---", ${cell_trab}=""))',
#                 #         'format': blue_bold_format
#                 #     })
#                 #
#                 #     cell_status = f'G{row_index + 1}'
#                 #
#                 #     worksheet.conditional_format(cell_status, {
#                 #         'type': 'formula',
#                 #         'criteria': f'=${cell_status}="APROVADO"',
#                 #         'format': green_bold_format
#                 #     })
#                 #
#                 #     worksheet.conditional_format(cell_status, {
#                 #         'type': 'formula',
#                 #         'criteria':
#                 #             f'=NOT(OR(${cell_status}!="APROVADO", ${cell_status}="---", ${cell_status}=""))',
#                 #         'format': red_bold_format
#                 #     })
#                 # Se a coluna 0 contiver as strings 'JUSTIFICATIVA' ou 'AVISO',
#                 # copia o conteúdo da linha e mescla as células das colunas 1 até 6
#                 # Se encontrar na coluna 0 (primeira coluna) as strings 'JUSTIFICATIVA' ou 'AVISO',
#                 # aplica formatação
#                 if (row.iloc[0] == 'JUSTIFICATIVA') or (row.iloc[0] == 'AVISO'):
#                     worksheet.write(row_index, 0, row.iloc[0], custom_format_1)
#                     # Se o tamanho do conteúdo da célula na coluna 1 for > do que 150 caracteres,
#                     # aumenta a altura da linha para 50
#                     if len(row.iloc[1]) > 150:
#                         worksheet.set_row(row_index, 50)
#                     # Mescla as colunas a partir da coluna 1 até a última coluna
#                     # matendo o conteúdo da célula da coluna 1 nas células mescladas
#                     worksheet.merge_range(
#                         row_index, 1, row_index, 6, row.iloc[1], custom_format_2)
#
#                 # Itera sobre as colunas e linhas
#                 for col_index, value in enumerate(row):
#                     # Se a coluna for a primeira (índice 0) e o conteúdo da célula da primeira
#                     # linha começar com a string 'PONTO DIGITAL', Formata os cabeçalhos
#                     # do início da planilha e entre os meses, aplicando borda e mesclando as células
#                     if col_index == 0 and value.startswith('PONTO DIGITAL'):
#                         worksheet.write(row_index, 0, row.iloc[0])
#                         worksheet.merge_range(
#                             row_index, 0, row_index, 6, value, header_format
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
#                     elif (col_index == 4
#                           and isinstance(value, str)
#                           and value < '12:00:00'
#                           and value != '---'
#                           and value != ''
#                     ):
#                         worksheet.write(row_index, col_index, value, blue_bold_format)
#
#                     # Se a célula da coluna 6 contiver a string 'APROVADO',
#                     # aplica formatação com a cor de fundo verde e cor da letra branca
#                     elif col_index == 6 and isinstance(value, str) and value == 'APROVADO':
#                         worksheet.write(row_index, col_index, value, green_bold_format)
#
#                 # Se o índice da coluna for < 7 e nela contiver a string 'DATA ENTRADA',
#                 # aplica formatação em toda a linha do cabeçalho das colunas
#                 for col in range(len(row)):
#                     if col < 7 and 'DATA ENTRADA' in row.values:
#                         worksheet.write(row_index, col, row.iloc[col], header_format)