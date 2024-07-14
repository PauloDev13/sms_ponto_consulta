import streamlit as st
from selenium import webdriver

from time import sleep

from services import authenticate
from utils import extrator_data, utils


# Configuração do título da página do Streamlit
st.set_page_config(page_title='PGM cont', page_icon=":bar_chart:")
st.title('Consulta ponto SMS')

def main():
    # Seta os valores iniciais dos campos no Session State
    if 'cpf' not in st.session_state:
        st.session_state.cpf = ''

    if 'date_start' not in st.session_state:
        st.session_state.date_start = None

    if 'date_end' not in st.session_state:
        st.session_state.date_end = None

    # Formulário para a digitação dos dados da pesquisa
    with st.form(key='form_date'):
        st.text_input('CPF', key='cpf', placeholder='Informe o CPF')
        # Divide o form em duas colunas
        col1, col2 = st.columns(2)

        with col1:
            st.date_input('Data de início:', key='date_start', format='DD/MM/YYYY')
            submit_button = st.form_submit_button(
                'Gerar arquivo', use_container_width=True,
                on_click=utils.form_callback
            )
        with col2:
            st.date_input('Data final:', key='date_end', format='DD/MM/YYYY')
            logout_button = st.form_submit_button(
                'Sair', use_container_width=True,
                on_click=authenticate.logout()
            )

if __name__ == '__main__':
    main()

#
#     if submit_button:
#         validate_cpf = utils.validate_cpf(st.session_state['cpf'])
#         valitade_dates = utils.validate_dates(st.session_state['date_start'], st.session_state['date_end'])
#         utils.clear_on_submit()
#
#         if validate_cpf and valitade_dates:
#             if len(st.session_state['cpf']) == 11:
#                 cpf_input = utils.format_cpf(st.session_state['cpf'])
#             # Verifica se existe uma sessão no Streamlit para o usuário logado
#             # Se NÃO, chama a função 'login' do módulo 'authenticate' que retorna uma instância do navegador
#             # Armazena a instância retornada numa sessão do Streamlit
#                 if validate_cpf:
#             # if 'driver' not in st.session_state:
#             #     if driver := authenticate.login():
#             #         st.session_state.driver = driver
#             #         driver.minimize_window()
#
#                     # Exibe um spinner até que a funçao 'data_fetch'
#                     # do módulo 'extrator_data' conclua a execução
#                     with st.spinner('Gerando arquivo...'):
#                         sleep(3)
#                         result = True
#                         # result = extrator_data.data_fetch(
#                         #     cpf_input, month_start, year_start, month_end, year_end, st.session_state.driver
#                         # )
#
#                     # Se a função retornar TRUE, o arquivo foi gerado com sucesso,
#                     # exibe mensagem de sucesso, espera 2 segundos e fecha a mensagem
#                     if result:
#                         utils.default_msg('Arquivo criado com sucesso!', 'success')
#
#             else:
#                 # Se já existir uma sessão aberta no Stremlit, repete o processo de geração do arquivo
#                 with st.spinner('Gerando arquivo...'):
#                     sleep(3)
#                     result = True
#                     # result = extrator_data.data_fetch(
#                     #     cpf_input, month_start, year_start, month_end, year_end, st.session_state.driver
#                     # )
#                 if result:
#                     utils.default_msg('Arquivo criado com sucesso!', 'success')
#
#
# if __name__ == '__main__':
#     main()