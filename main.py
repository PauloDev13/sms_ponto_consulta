import streamlit as st
# from pesquisa import realizar_pesquisa
from services import authenticate
from utils import extrator_data

# Configuração da página do Streamlit
st.set_page_config(page_title="Extrator de Dados", page_icon=":bar_chart:")
st.title("Extrator de Dados")

# Formulário para o intervalo de datas
with st.form(key="form_datas"):
    cpf = st.text_input(key='cpf', label='CPF', placeholder='Informe o CPF (ex: 100.200.300-40)')
    col1, col2 = st.columns(2)
    with col1:
        date_start = st.date_input("Data de início:")
    with col2:
        date_end = st.date_input("Data final:")

    submit_button = st.form_submit_button(label="Pesquisar")

# Execução da pesquisa
if submit_button:
    # Extração de mês e ano das datas
    month_start = date_start.month
    year_start = date_start.year
    month_end = date_end.month
    year_end = date_end.year

    if authenticate.login():
        with st.spinner('Realizando pesquisa...'):
            result = extrator_data.data_fetch(cpf, month_start, year_start, month_end, year_end)
        if result:
            st.success("Pesquisa concluída! Verifique o arquivo 'dados_pesquisa.xlsx'.")
