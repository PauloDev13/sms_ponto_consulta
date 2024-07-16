import streamlit as st

from time import sleep

from services import authenticate
from utils import extrator_data


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
        cpf = ''.join(filter(str.isdigit, cpf))

        if not cpf:
            default_msg('O campo CPF é obrigatório!', 'info')
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
        if len(cpf_input) == 11:
            cpf_input = format_cpf(cpf_input)

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
                    result = extrator_data.data_fetch(
                        cpf_input, month_start, year_start, month_end, year_end, st.session_state.driver
                    )

                # Se a função retornar TRUE, o arquivo foi gerado com sucesso,
                # limpa os campos do formulário e exibe mensagem de sucesso
                if result:
                    default_msg('Arquivo criado com sucesso!', 'success')
                    # Limpa o formulário
                    # fields_clear()


        else:
            # Se já existir uma sessão aberta no Stremlit, repete o processo de geração do arquivo
            with st.spinner('Gerando arquivo...'):
                result = extrator_data.data_fetch(
                    cpf_input, month_start, year_start, month_end, year_end, st.session_state.driver
                )

            # Se a função retornar TRUE, o arquivo foi gerado com sucesso,
            # limpa os campos do formulário e exibe mensagem de sucesso
            if result:
                default_msg('Arquivo criado com sucesso!', 'success')
                # Limpa o formulário
                # fields_clear()
