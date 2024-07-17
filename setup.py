import streamlit as st
import pandas
import selenium
import xlsxwriter
import dotenv
import lxml
import openpyxl
import html5lib
from bs4 import BeautifulSoup
import streamlit.web.cli as stcli
import os, sys

import logging

# Configurando logs
logging.basicConfig(level=logging.DEBUG, filename="setup.log", filemode='w')
logging.debug("Iniciando setup.py")


def resolver_path(path):
    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path

if __name__ == '__main__':
    sys.argv = [
        'streamlit',
        'run',
        resolver_path('main.py'),
        '--global.developmentMode=false'
    ]
    sys.exit(stcli.main())

logging.debug("Finalizando setup.py")

# import sys
# from cx_Freeze import setup, Executable
#
# # Definindo a base corretamente para aplicações web
# base = None
# if sys.platform == 'win32':
#     base = None  # Aplicação web não requer 'Win32GUI'
#
# # Função auxiliar para verificar se um módulo está disponível
# def module_exists(module_name):
#     spec = importlib.util.find_spec(module_name)
#     return spec is not None
#
# build_exe_options = {
#     'packages': [
#         'streamlit',
#         'pandas',
#         'selenium',
#         'html5lib',
#         'bs4',
#         'numpy',
#         'numpy.core',
#         'xlsxwriter',
#         'lxml',
#         'openpyxl'
#     ],
#     'include_files': [
#         '.env',
#         'main.py',
#         'run_streamlit.py',
#         ('utils/__init__.py', 'utils/__init__.py'),
#         ('utils/extractor_data.py', 'utils/extractor_data.py'),
#         ('utils/utils.py', 'utils/utils.py'),
#         ('services/__init__.py', 'services/__init__.py'),
#         ('services/authenticate.py', 'services/authenticate.py'),
#         # Adicione outros arquivos necessários
#     ],
#     'bin_path_includes': [
#         # Inclua caminhos para DLLs se necessário
#     ],
#     'excludes': [
#         'tkinter',  # Excluir tkinter se não for necessário
#     ],
# }
#
# setup(
#     name='sms_ponto_digital_consulta',
#     version='0.1',
#     description='Descrição da aplicação',
#     options={'build_exe': build_exe_options},
#     executables=[Executable('main.py', base=base, target_name='sms_ponto.exe')]
# )
