import streamlit as st

import pandas as pd

import os
from datetime import datetime
from time import sleep
from dotenv import load_dotenv

from services import authenticate
from utils import extractor_data

load_dotenv()
file_path = os.getenv('PATH_FILE_BASE')


# Função para verificar se a string está no formato correto ('00:00:00')
def format_validation(hour_str) -> bool:
    try:
        datetime.strptime(hour_str, '%H:%M:%S')
        return True
    except ValueError:
        return False


# Função para converter string para datetime.time
def str_to_time(hour_str):
    try:
        return datetime.strptime(hour_str, '%H:%M:%S').time()
    except ValueError:
        return None


# Atualiza as colunas 'HT', 'HJ', 'ST' se nas colunas 'TRABALHADA' e
# 'HORA JUSTIFICADA' os valores forem iguais ou maiores que '12:00:00'.
# Na coluna 'STATUS' se o valor for igual a 'APROVADO'
def columns_update(row):
    try:
        # Se os dados da coluna 'TRABALHADA' estiver no formado '00:00:00',
        # faz a conversão para datetime.time. Se não, retorna None
        if format_validation(row['TRABALHADA']):
            hour_worked = str_to_time(row['TRABALHADA'])
        else:
            hour_worked = None

        # Se a HORA TRABALHADA não for None e for maior ou igual a '12:00:00',
        # retorna 1, se não, retorna uma string vazia ('')
        ht_value = 1 if hour_worked and hour_worked >= str_to_time('12:00:00') else ''

        # Se os dados da coluna 'HORA JUSTIFICADA' estiver no formado '00:00:00',
        # faz a conversão para datetime.time. Se não, retorna None
        if format_validation(row['HORA JUSTIFICADA']):
            hour_justified = str_to_time(row['HORA JUSTIFICADA'])
        else:
            hour_justified = None

        # Se a HORA JUSTIFICADA não for None e for maior ou igual a '12:00:00',
        # retorna 1, se não, retorna uma string vazia ('')
        hj_value = 1 if hour_justified and hour_justified >= str_to_time('12:00:00') else ''

        # Se os horários de entrada e saída forem diferentes de None e
        # o horário de entrada for maior ou igual a '18:00:00' e
        # o horário de saída for maior ou igual a '05:00:00', retorna 1,
        # se não, retorna string vazia ('')
        if format_validation(row['ENTRADA']):
            tn_night_work_start = str_to_time(row['ENTRADA'])
        else:
            tn_night_work_start = None

        if format_validation(row['SAÍDA']):
            tn_night_work_end = str_to_time(row['SAÍDA'])
        else:
            tn_night_work_end = None

        tn_night_work = 1 if (
                (tn_night_work_start and tn_night_work_end)
                and (tn_night_work_start >= str_to_time('18:00:00')
                     and tn_night_work_end >= str_to_time('05:00:00'))

        ) else ''

        # Se os dados na coluna 'STATUS' for igual à string 'APROVADO',
        # retorna 1, se não, retorna uma string vazia ('')
        st_value = 1 if row['STATUS'] == 'APROVADO' else ''

        # Monta a (Series) com as colunas e os valores que passaram na validação
        return pd.Series({
            'HT': ht_value,
            'HJ': hj_value,
            'ST': st_value,
            'ADN': tn_night_work
        })
    except Exception as e:
        print(f"Erro: {e}")

        # return
        # pd.Series({'HT': '', 'HJ': '', 'ST': ''})


# Função que insere '.' e '-' no número do CPF, caso tenha sido
# informado somente números.
def format_cpf(cpf: str) -> str:
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'


# Instancia mensagem de alerta de acordo com os parâmetros informados
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
        default_msg('Erro na mensagem', 'error')
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

        # Valida as datas
        dates_valid = validate_dates(date_start, date_end)

    # Se datas e CPF forem válidas, extrai os meses e anos de inícial e final
    if cpf_valid and dates_valid:
        month_start = date_start.month
        year_start = date_start.year
        month_end = date_end.month
        year_end = date_end.year

        # Verifica se existe uma sessão no Streamlit para o usuário logado
        # Se NÃO, chama a função 'login' do módulo 'authenticate'
        # que retorna uma instância do navegador e armazena a instância
        # retornada na sessão do Streamlit
        if 'driver' not in st.session_state:
            if driver := authenticate.login():
                driver.minimize_window()
                st.session_state.driver = driver
                st.session_state['driver'] = driver

                # Exibe um spinner até que a funçao 'data_fetch'
                # do módulo 'extrator_data' conclua a execução
                with st.spinner(f'Processamento em andamento, AGUARDE...'):
                    extractor_data.data_fetch(
                        cpf_input, month_start, year_start, month_end, year_end, st.session_state.driver
                    )

                # Se não houver erros no processamento, exibe mensagem de sucesso
                default_msg('Arquivo criado com sucesso!', 'success')

        else:
            # Se já existir uma sessão aberta no Streamlit, repete o processo de geração do arquivo
            with st.spinner('Processamento em andamento, AGUARDE...'):
                extractor_data.data_fetch(
                    cpf_input, month_start, year_start, month_end, year_end, st.session_state.driver
                )

            # Se não houver erros no processamento, exibe mensagem de sucesso
            default_msg('Arquivo criado com sucesso!', 'success')

