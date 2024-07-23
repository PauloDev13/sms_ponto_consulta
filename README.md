## Criando executável do projeto com Streamlit usando a biblioteca cx_Freeze.

**1 - Criar na raiz do projeto o arquivo 'setup.py' e importar
    nele TODAS as bibliotecas e módulos locais como foram 
    importados nos módulos. Veja no exemplo abaixo:**

**Arquivo setpu.py**
    
    # IMPORTS DAS BIBLIOTECAS
    import streamlit as st
    import streamlit.web.cli as stcli
    import streamlit.runtime.scriptrunner.magic_funcs
    import pandas as pd
    import selenium
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import (
        TimeoutException,
        NoSuchWindowException,
        ElementClickInterceptedException)
    from selenium.webdriver.support import expected_conditions as ec
    import logging
    import os, sys
    ... demais bibliotecas.

    # IMPORTS DOS MÓDULOS LOCAIS
    from services import authenticate
    from utils import utils
    from utils import extractor_data


    # Configurando logs
    logging.basicConfig(level=logging.DEBUG, filename="setup.log", filemode='w')
    logging.debug("Iniciando setup.py")

    # FUNÇÃO PRINCIPAL

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

    '****** Fim do Arquivo setup.py ********'

**2 - Usar o comando abaixo no prompt a partir da raiz do projeto**

    cxfreeze --script setup.py (compila o aplicativo streamlit e cria o executável)

**3 - Será crianda na raiza do projeto a pasta 'build' e dentro dela a pasta com arquivos e o
    executável 'setup.exe'.**

**4 - Copie para dentro dessa pasta todos os arquivos e pastas usadas no projeto.
    Ex: Arquivos: '.env' (variáveis usadas no projeto), arquivos estáticos (.jpeg, bmp, etc.).
    Pastas: (utils, service, etc) ou seja, toda a estrutura de pastas do projeto
    com todos os arquivos '.py' existentes.**

**5 - Agora é só executar o setup.exe para abrir o aplicativo com Streamlit.**