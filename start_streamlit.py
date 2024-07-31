import os
import sys
# import streamlit.web.cli as stcli
import logging

# Configurando logs
logging.basicConfig(level=logging.DEBUG, filename="start_streamlit.log", filemode='w')

logging.debug("Iniciando start_streamlit.py")


def resolver_path(path):
    logging.debug(f"Resolvendo caminho para: {path}")

    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))

    logging.debug(f"Caminho definido para: {resolved_path}")

    return resolved_path


def iniciar_streamlit():
    logging.debug("Verificando se Streamlit já está em execução")

    if 'streamlit' not in sys.argv:

        logging.debug("Iniciando o Streamlit via stcli.main()")

        sys.argv = [
            'streamlit',
            'run',
            resolver_path('main.py'),
            '--global.developmentMode=false'
        ]

        logging.debug(f"sys.argv set to: {sys.argv}")

        sys.exit(stcli.main())
    else:
        logging.debug("Streamlit já está em execução")


if __name__ == '__main__':
    logging.debug("Entrou no bloco __main__")

    iniciar_streamlit()
