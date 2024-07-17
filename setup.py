import sys
from cx_Freeze import setup, Executable

# Definindo a base corretamente para aplicações web
base = None
if sys.platform == 'win32':
    base = None  # Aplicação web não requer 'Win32GUI'

build_exe_options = {
    'packages': [
        'streamlit',
        'pandas',
        'selenium',
        'html5lib',
        'bs4',
        'numpy',
        'numpy.core',
        'xlsxwriter',
        'lxml',
        'openpyxl'
    ],
    'include_files': [
        '.env',
        ('utils/__init__.py', 'utils/__init__.py'),
        ('utils/extractor_data.py', 'utils/extractor_data.py'),
        ('utils/utils.py', 'utils/utils.py'),
        ('services/__init__.py', 'services/__init__.py'),
        ('services/authenticate.py', 'services/authenticate.py'),
        # Adicione outros arquivos necessários
    ],
    'bin_path_includes': [
        # Inclua caminhos para DLLs se necessário
    ],
    'excludes': [
        'tkinter',  # Excluir tkinter se não for necessário
    ],
}

setup(
    name='sms_ponto_digital_consulta',
    version='0.1',
    description='Descrição da aplicação',
    options={'build_exe': build_exe_options},
    executables=[Executable('main.py', base=base, target_name='main.exe')]
)
