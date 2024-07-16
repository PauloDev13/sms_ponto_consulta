import streamlit as st
from selenium import webdriver

from time import sleep

from services import authenticate
from utils import extrator_data, utils


# Configuração do título da página do Streamlit
st.set_page_config(page_title='PGM cont', page_icon=":bar_chart:")
st.title('Consulta ponto SMS')

def main():
    # Formulário para a digitação dos dados da pesquisa
    with st.form(key='form_date'):
        st.text_input('CPF', key='cpf', placeholder='Informe o CPF', value='')
        # Divide o form em duas colunas
        col1, col2 = st.columns(2)

        with col1:
            st.date_input('Data de início:', key='date_start', format='DD/MM/YYYY', value=None)
            # st.form_submit_button(
            #     'Gerar arquivo', use_container_width=True,
            #     on_click=utils.form_callback
            # )
        with col2:
            st.date_input('Data final:', key='date_end', format='DD/MM/YYYY', value=None)
            # logout_button = st.form_submit_button(
            #     'Sair', use_container_width=True,
            # )

        col3, col4, col5 = st.columns(3)

        with col3:
            submit_button = st.form_submit_button(
                'Gerar arquivo', use_container_width=True
                )
        with col4:
            st.form_submit_button(
                'Limpar', use_container_width=True,
                on_click=utils.fields_clear)
        with col5:
            logout_button = st.form_submit_button(
                'Sair', use_container_width=True
            )

        # # Fecha a Session State e encerra o navegador
        if logout_button:
            authenticate.logout()

        # Chama a função principal da aplicação
        if submit_button:
            utils.form_callback()

        # if submit_button:
        #     cpf_input = st.session_state['cpf']
        #     date_start = st.session_state['date_start']
        #     date_end = st.session_state['date_end']
        #
        #     # Valida o CPF
        #     cpf_valid = utils.validate_cpf(cpf_input)
        #
        #     # Se o CPF for válido e tiver 11 números, formata aplicando uma máscara
        #     if cpf_valid:
        #         if len(cpf_input) == 11:
        #             cpf_input = utils.format_cpf(cpf_input)
        #
        #         # Valida as datas
        #         dates_valid = utils.validate_dates(date_start, date_end)
        #
        #     # Se datas e CPF forem válidas, extrai os meses e anos de inícil e final
        #     if cpf_valid and dates_valid:
        #         month_start = date_start.month
        #         year_start = date_start.year
        #         month_end = date_end.month
        #         year_end = date_end.year
        #
        #         # Verifica se existe uma sessão no Streamlit para o usuário logado
        #         # Se NÃO, chama a função 'login' do módulo 'authenticate' que retorna uma instância do navegador
        #         # Armazena a instância retornada numa sessão do Streamlit
        #         if 'driver' not in st.session_state:
        #             if driver := authenticate.login():
        #                 st.session_state.driver = driver
        #                 st.session_state['driver'] = driver
        #                 driver.minimize_window()
        #
        #                 # Exibe um spinner até que a funçao 'data_fetch'
        #                 # do módulo 'extrator_data' conclua a execução
        #                 with st.spinner('Gerando arquivo...'):
        #                     result = extrator_data.data_fetch(
        #                         cpf_input, month_start, year_start, month_end, year_end, st.session_state.driver
        #                     )
        #
        #                 # Se a função retornar TRUE, o arquivo foi gerado com sucesso,
        #                 # limpa os campos do formulário e exibe mensagem de sucesso
        #                 if result:
        #                     utils.default_msg('Arquivo criado com sucesso!', 'success')
        #
        #
        #         else:
        #             # Se já existir uma sessão aberta no Stremlit, repete o processo de geração do arquivo
        #             with st.spinner('Gerando arquivo...'):
        #                 result = extrator_data.data_fetch(
        #                     cpf_input, month_start, year_start, month_end, year_end, st.session_state.driver
        #                 )
        #
        #             # Se a função retornar TRUE, o arquivo foi gerado com sucesso,
        #             # limpa os campos do formulário e exibe mensagem de sucesso
        #             if result:
        #                 utils.default_msg('Arquivo criado com sucesso!', 'success')


if __name__ == '__main__':
    main()