## Criando executável do projeto com Streamlit usando a biblioteca cx_Freeze.

**1 - Criar na raiz do projeto os arquivos 'setup.py' e 'start_streamlit.py'.**

### setup.py
    # Imports das bibliotecas usadas no arquivo
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

### start_streamlit.py
    # Imports das bibliotecas usadas no arquivo
    import os
    import sys
    import streamlit.web.cli as stcli
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

**2 - Usar o comando abaixo no prompt a partir da raiz do projeto**

    python setup.py build

*O comando compila o aplicativo streamlit, cria o executável e monta a estrutura
pastas e arquivos necessários para a execução correta do aplicativo.*

**3 - Será crianda na raiz do projeto a pasta 'build' e dentro dela a estrutura com todas as
pastas, arquivos e o executável. A estrutura terá que ser exatamente igual ao do
projeto. Essa estrutura é definida nas configurações 'include_files[] do arquivo setup.py**

**4 - Acesse a pasta 'build' e abra o arquivo executável clicando 2 vezes sobre ele. A
aplicação Streamlit deverá abrir no navegador padrão, sem exibir a janela (console) do
servidor do Streamlit.**

## 5 - IMPORTANTE:
**Para o sucesso da compilação e a correta execução do aplicativo com Streamlit através de
um arquivo 'executável', é necessário que as configurações nas TAGs 'packages[]', 'includes[]'
e include_files[] devem estar absolutamente corretas**

### packages[
    'streamlit', 
    'pandas', 
    'outras bibliotecas'
]

***Devem ser incluídas todas as bibliotecas instaladas e usadas no projeto.***
### includes[
    'streamlit.web.cli', "dotenv"
]

***Devem ser incluídos módulos específicos de bibliotecas usados no projeto.***
### include_files[
    ('utils', 'utils'), -> pasta utils da raiz do projeto, para a raiz da pasta build
    ('services', 'services'), -> pasta services da raiz do projeto, para a raiz da pasta build
    ('.env', '.env'), -> arquivo .env da raiz do projeto, para a raiz da pasta build
    ('main.py', 'main.py'),-> arquivo main.py da raiz do projeto, para a raiz da pasta build
    ('start_streamlit.py', 'start_streamlit.py') -> arquivo start_streamlit.py da raiz do 
                                                    projeto, para a raiz da pasta build
]

***Devem ser incluídos em 'TUPLAS', o caminho para os arquivos e pastas do projeto e o 
caminho onde esses arquivos e pastas ficarão na pasta build. É altamente recomendável que
os caminhos devam ser os mesmos.***