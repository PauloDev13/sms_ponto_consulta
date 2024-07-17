import subprocess
import sys

# Verifique o caminho para o Python executável
python_executable = sys.executable

# Execute o comando `streamlit run main.py`
subprocess.run([python_executable, '-m', 'streamlit', 'run', 'main.py'])
