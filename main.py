import streamlit as st
from selenium import webdriver

from time import sleep

from services import authenticate
from utils import extrator_data, utils


# Configuração do título da página do Streamlit
st.set_page_config(page_title='PGM cont', page_icon=":bar_chart:")
st.title('Consulta ponto SMS')

# Formulário para a digitação dos dados da pesquisa
with st.form(key='form_date'):
    cpf_input = st.text_input('CPF', key='cpf', placeholder='Informe o CPF',
    )
    # Divide o form em duas colunas
    col1, col2 = st.columns(2)

    with col1:
        date_start = st.date_input('Data de início:', key='date_start', format='DD/MM/YYYY')
        submit_button = st.form_submit_button('Gerar arquivo', use_container_width=True)
    with col2:
        date_end = st.date_input('Data final:', key='date_end', format='DD/MM/YYYY')
        logout_button = st.form_submit_button('Sair', use_container_width=True)

    # Extração de mês e ano das datas
    month_start = date_start.month
    year_start = date_start.year
    month_end = date_end.month
    year_end = date_end.year

    if logout_button:
        authenticate.logout()

    if submit_button:
        validate_cpf = utils.validate_cpf(cpf_input)
        valitade_dates = utils.validate_dates(date_start, date_end)

        if validate_cpf and valitade_dates:
            if len(cpf_input) == 11:
                cpf_input = utils.format_cpf(cpf_input)
            # Verifica se existe uma sessão no Streamlit para o usuário logado
            # Se NÃO, chama a função 'login' do módulo 'authenticate' que retorna uma instância do navegador
            # Armazena a instância retornada numa sessão do Streamlit
            if 'driver' not in st.session_state:
                if driver := authenticate.login():
                    st.session_state.driver = driver
                    driver.minimize_window()

                    # Exibe um spinner até que a funçao 'data_fetch'
                    # do módulo 'extrator_data' conclua a execução
                    with st.spinner('Gerando arquivo...'):
                        result = extrator_data.data_fetch(
                            cpf_input, month_start, year_start, month_end, year_end, st.session_state.driver
                        )

                    # Se a função retornar TRUE, o arquivo foi gerado com sucesso,
                    # exibe mensagem de sucesso, espera 2 segundos e fecha a mensagem
                    if result:
                        utils.default_msg('Arquivo criado com sucesso!', 'success')

            else:
                # Se já existir uma sessão aberta no Stremlit, repete o processo de geração do arquivo
                with st.spinner('Gerando arquivo...'):
                    result = extrator_data.data_fetch(
                        cpf_input, month_start, year_start, month_end, year_end, st.session_state.driver
                    )
                if result:
                    utils.default_msg('Arquivo criado com sucesso!', 'success')


