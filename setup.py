import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

build_exe_options = {
    'packages': [
        "streamlit",
        "pandas",
        "selenium",
        "html5lib",
        "bs4",
        "numpy",
        "numpy.core"
    ],
    'include_files': [
        (".env", ".env"),
        ('utils/__init__.py', 'utils/__init__.py'),
        ('utils/extrator_data.py', 'utils/extrator_data.py'),
        ('utils/utils.py', 'utils/utils.py'),
        ('services/__init__.py', 'services/__init__.py'),
        ('services/authenticate.py', 'services/authenticate.py'),
        # ... outros arquivos ...
    ],
    'bin_path_includes': [
        # ... caminhos para DLLs (se necessário) ...
    ]
}

setup(
    name="sms_ponto_digital_consulta",
    version="0.1",
    description="Descrição da aplicação",
    options={'build_exe': build_exe_options},
    executables=[Executable("main.py", base=base)]
)