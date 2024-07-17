import streamlit as st

from services import authenticate
from utils import utils

import logging

# Configurando logs
logging.basicConfig(level=logging.DEBUG, filename="main.log", filemode='w')
logging.debug("Iniciando main.py")


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

if __name__ == '__main__':
    main()