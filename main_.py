import streamlit as st
from selenium import webdriver

from time import sleep

from services import authenticate
from utils import extrator_data

# Configuração da página do Streamlit
st.set_page_config(page_title='PGM cont', page_icon=":bar_chart:")
st.title('Consulta ponto SMS')


# Formulário para o intervalo de datas
with st.form(key='form_date'):
    cpf = st.text_input(key='cpf', label='CPF', placeholder='Informe o CPF (ex: 100.200.300-40)')

    col1, col2 = st.columns(2)
    with col1:
        date_start = st.date_input('Data de início:', format='DD/MM/YYYY')
    with col2:
        date_end = st.date_input('Data final:', format='DD/MM/YYYY')
    with col1:
        new_search = st.checkbox("Gerar novo arquivo?")

    submit_button = st.form_submit_button(label='Gerar arquivo')

    # Extração de mês e ano das datas
    month_start = date_start.month
    year_start = date_start.year
    month_end = date_end.month
    year_end = date_end.year

    if submit_button:
        # Verifica se o usuário está logado
        if 'driver' not in st.session_state:
            if driver := authenticate.login():
                # Armazena o driver na sessão
                st.session_state.driver = driver

                with st.spinner('Gerando arquivo...'):
                    result = extrator_data.data_fetch(
                        cpf, month_start, year_start, month_end, year_end, st.session_state.driver
                    )
                if result:
                    success = st.success('Arquivo criado com sucesso!')
                    sleep(2)
                    success.empty()

        else:
            print('JÁ EXISTE SESSÃO ABERTA')

            if new_search:
                # print('ENTRA O CÓDIGO PARA NOVAS CONSULTAS SEM NOVO LOGIN')
                with st.spinner('Gerando arquivo...'):
                    result = extrator_data.data_fetch(
                        cpf, month_start, year_start, month_end, year_end, st.session_state.driver
                    )
                if result:
                    success = st.success('Arquivo criado com sucesso!')
                    sleep(2)
                    success.empty()

st.stop()

