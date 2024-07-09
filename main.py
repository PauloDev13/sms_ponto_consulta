import streamlit as st
# from pesquisa import realizar_pesquisa
# from login import fazer_login

# Configuração da página do Streamlit
st.set_page_config(page_title="Extrator de Dados", page_icon=":bar_chart:")
st.title("Extrator de Dados")

# Formulário para o intervalo de datas
with st.form(key="form_datas"):
    col1, col2 = st.columns(2)
    with col1:
        date_start = st.date_input("Data de início:")
    with col2:
        date_end = st.number_input("Data final:")

    submit_button = st.form_submit_button(label="Pesquisar")

# Execução da pesquisa
if submit_button:
    # Extração de mês e ano das datas
    month_start = date_start.month
    year_start = date_start.year
    month_end = date_end.month
    year_end = date_end.year

    if login():
        with st.spinner('Realizando pesquisa...'):
            resultado = data_fetch(cpf, mes_inicio, ano_inicio, mes_fim, ano_fim)
        if resultado:
            st.success("Pesquisa concluída! Verifique o arquivo 'dados_pesquisa.xlsx'.")
