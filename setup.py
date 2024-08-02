from cx_Freeze import setup, Executable

import os, sys

# Configurações do cx_Freeze
build_exe_options = {
    "packages": [
        "os", "sys", "streamlit", "psutil",
        "pandas", "selenium",
        "xlsxwriter", "bs4"
    ],
    "includes": ["streamlit.web.cli", "dotenv"],
    "include_files": [
        ('utils', 'utils'),
        ('services', 'services'),
        ('PLANILHAS_SMS', 'PLANILHAS_SMS'),
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
        target_name="app_sms.exe"
    )
]

setup(
    name="PontoSMSApp",
    version="0.1",
    description="Aplicativo Streamlit",
    options={"build_exe": build_exe_options},
    executables=executables
)
