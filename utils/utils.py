import streamlit as st

from time import sleep


# Função que insere '.' e '-' no número do CPF, caso tenha sido
# informado somente números.
def format_cpf(cpf: str) -> str:
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'


# Instancia mensagem de alerta de acordo com os parâmetro informados
def default_msg(msg: str, type_msg: any):
    try:
        match type_msg:
            case 'success':
                type_msg = st.success(msg, icon='👍')
            case 'warning':
                type_msg = st.warning(msg, icon='👊')
            case 'info':
                type_msg = st.info(msg, icon='👆')
            case _:
                type_msg = st.error(msg, icon='👎')
            # case 'error' :
            #     type_msg = st.error(msg, icon='👎')
        sleep(3)
        type_msg.empty()
        return type_msg

    except Exception as ex:
        utils.default_msg('Erro na messege', 'error')
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
            default_msg('A data de início não pode ser posterior à data final!', 'error')
            return False
        return True
    except Exception as ex:
        utils.default_msg('Erro ao validar datas', 'error')
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
        utils.default_msg('Erro ao validar CPF', 'error')
        print(f'Erro stacktrace: {ex}')