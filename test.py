import streamlit as st

import utils.utils
from utils import utils

# def validate_slider(num: int):
#     return num >= 5
#
#
# def validate_checkbox(bol: bool):
#     return True if bol else False


with st.form(key='form'):
    st.slider('Barra', 0, 15, 0, key='my_slider')
    st.checkbox('Sim ou Não', key='my_checkbox')
    st.form_submit_button('Submit', on_click=utils.form_callback)



# def form_callback():
#     slider_valid = validate_slider(st.session_state['my_slider'])
#     checkbox_valid = validate_checkbox(st.session_state['my_checkbox'])
#
#     if not slider_valid:
#         st.error('O slider deve ser maior 5')
#
#     elif not checkbox_valid:
#         st.error('Marque o checkbox')
#
#     else:
#         slider_input = st.session_state['my_slider']
#         checkbox_input = st.session_state['my_checkbox']
#
#         st.write(f'VALOR DO SLIDE: {slider_input}')
#         st.write(f'VALOR DO SLIDE: {checkbox_input}')
#
#         st.session_state['my_slider'] = 0
#         st.session_state['my_checkbox'] = False
#
#         st.write(f'VALOR2 DO SLIDE: {st.session_state['my_slider']}')
#         st.write(f'VALOR2 DO SLIDE: {st.session_state['my_checkbox']}')


# if __name__ == '__main__':
#     test()

# def validate_username(username):
#     # Validação básica para username: deve ter pelo menos 5 caracteres
#     return len(username) >= 5
#
#
# def validate_password(password):
#     # Validação básica para password: deve ter pelo menos 8 caracteres
#     return len(password) >= 8
#
#
# def main():
#     st.title('Formulário de Login2')
#
#     # Inicializar o estado dos campos e do botão de submissão
#     if 'username' not in st.session_state:
#         st.session_state.username = ''
#     if 'password' not in st.session_state:
#         st.session_state.password = ''
#     if 'is_submit_disabled' not in st.session_state:
#         st.session_state.is_submit_disabled = True
#
#     # Campos do formulário
#     username = st.text_input('Username', key='username')
#     password = st.text_input('Password', type='password', key='password')
#
#     # Função de callback para validação e submissão
#     def validate_and_submit():
#         username_valid = validate_username(st.session_state.username)
#         password_valid = validate_password(st.session_state.password)
#
#         if not username_valid:
#             st.error('O username deve ter pelo menos 5 caracteres.')
#             st.session_state.username = ''
#
#         if not password_valid:
#             st.error('A senha deve ter pelo menos 8 caracteres.')
#             st.session_state.password = ''
#
#         if username_valid and password_valid:
#             st.success('Formulário submetido com sucesso!')
#             st.session_state.is_submit_disabled = True
#             st.session_state.username = ''
#             st.session_state.password = ''
#
#     # Verificar a validação dos campos
#     username_valid = validate_username(st.session_state.username)
#     password_valid = validate_password(st.session_state.password)
#
#     st.session_state.is_submit_disabled = not (username_valid and password_valid)
#
#     # Botão de submissão
#     submit_button = st.button('Submit', disabled=st.session_state.is_submit_disabled, on_click=validate_and_submit)
#
#
# if __name__ == '__main__':
#     main()
