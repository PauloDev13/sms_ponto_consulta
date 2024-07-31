from cx_Freeze import setup, Executable

import os, sys
import logging

# Configurando logs
logging.basicConfig(level=logging.DEBUG, filename="setup.log", filemode='w')
logging.debug("Iniciando setup.py")

# Configurações do cx_Freeze
build_exe_options = {
    "packages": [
        "os", "sys", "streamlit",
        "pandas", "selenium",
        "xlsxwriter", "bs4"
    ],
    "includes": ["streamlit.web.cli", "dotenv"],
    "include_files": [
        ('utils', 'utils'),
        ('services', 'services'),
        ('.env', '.env'),
        ('main.py', 'main.py'),
        ('start_streamlit.py', 'start_streamlit.py')
    ],
    "excludes": []
}

# Define o executável, com base em Win32GUI para ocultar o console
executables = [
    Executable(
        script="start_streamlit.py",
        base="Win32GUI" if sys.platform == "win32" else None,
        target_name="ponto_sms_app.exe"
    )
]

setup(
    name="PontoSMSApp",
    version="0.1",
    description="Aplicativo Streamlit",
    options={"build_exe": build_exe_options},
    executables=executables
)

logging.debug("Finalizando setup.py")
# Código de inicialização do Streamlit


# def resolver_path(path):
#     resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
#     return resolved_path
#
# if __name__ == '__main__':
#     sys.argv = [
#         'streamlit',
#         'run',
#         resolver_path('main.py'),
#         '--global.developmentMode=false'
#     ]
#     sys.exit(stcli.main())
#
