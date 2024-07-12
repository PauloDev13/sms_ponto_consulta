# import streamlit as st
#
#
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
