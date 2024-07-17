import subprocess
import sys
import logging
import os

import streamlit

# Definindo o diretório de logs
log_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
log_file = os.path.join(log_dir, "run_streamlit.log")

# Garantir que o diretório de logs exista
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configurando logs
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='w')
logging.debug("Iniciando run_streamlit.py")
print("Iniciando run_streamlit.py")

# Verifique o caminho para o Python executável
python_executable = sys.executable
logging.debug(f"Python executável: {python_executable}")
print(f"Python executável: {python_executable}")

# Verifique se o main.py está no local esperado
main_py_path = os.path.join(log_dir, 'main.py')
if not os.path.exists(main_py_path):
    logging.error(f"main.py não encontrado em {main_py_path}")
    print(f"main.py não encontrado em {main_py_path}")
else:
    logging.debug(f"main.py encontrado em {main_py_path}")
    print(f"main.py encontrado em {main_py_path}")

try:
    import streamlit

    logging.debug(f"Streamlit versão: {streamlit.__version__}")
    print(f"Streamlit versão: {streamlit.__version__}")
except ImportError as e:
    logging.error(f"Streamlit não encontrado: {e}")
    print(f"Streamlit não encontrado: {e}")

try:
    # Execute o comando `streamlit run main.py`
    result = subprocess.run([python_executable, '-m', 'streamlit', 'run', 'main.py'], check=True)
    logging.debug(f"Resultado do subprocess: {result}")
    print(f"Resultado do subprocess: {result}")
except Exception as e:
    logging.error(f"Erro ao executar subprocess: {e}")
    print(f"Erro ao executar subprocess: {e}")
    result = None

logging.debug("Fim do script run_streamlit.py")
print("Fim do script run_streamlit.py")
