import streamlit as st
from selenium import webdriver

from services import authenticate
from utils import extrator_data

# Configuração da página do Streamlit
st.set_page_config(page_title='PGM cont', page_icon=":bar_chart:")
st.title('Consulta ponto SMS')

# Verifica se o usuário está logado
if 'driver' not in st.session_state:
    if (driver := authenticate.login()):
        st.session_state.driver = driver  # Armazena o driver na sessão
        st.success("Login realizado com sucesso!")
    else:
        st.error("Erro ao fazer login. Verifique suas credenciais.")
else:
    st.info("Você já está logado.")
    st.button("Logout", on_click=logout)  # Botão de logout (opcional)
    st.stop()

if 'driver' in st.session_state:
    # Formulário para o intervalo de datas
    with st.form(key='form_date'):
        col1, col2 = st.columns(2)

        cpf = st.text_input(key='cpf', label='CPF', placeholder='Informe o CPF (ex: 100.200.300-40)')
        with col1:
            date_start = st.date_input('Data de início:', format='DD/MM/YYYY')
        with col2:
            date_end = st.date_input('Data final:', format='DD/MM/YYYY')
        with col1:
            new_seach = st.checkbox("Gerar novo arquivo?")
        submit_button = st.form_submit_button(label='Gerar arquivo')

    # Opção para o usuário escolher caso deseje realizar uma nova pesquisa

    # Execução da pesquisa
    if submit_button:
        # Extração de mês e ano das datas
        month_start = date_start.month
        year_start = date_start.year
        month_end = date_end.month
        year_end = date_end.year


        with st.spinner('Gerando arquivo...'):
            result = extrator_data.data_fetch(
                cpf, month_start, year_start, month_end, year_end, st.session_state.driver
            )
        if result:
            st.success('Arquivo criado com sucesso!')

    if not new_seach:
        logout()


else:
    st.warning("Você precisa fazer login para realizar a pesquisa.")


# Função para realizar logout (opcional)
def logout():
    if 'driver' in st.session_state:
        st.session_state.driver.quit()
        del st.session_state.driver
        st.success("Logout realizado com sucesso!")