import os
import sys
import streamlit.web.cli as stcli


def resolver_path(path):
    resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path


def iniciar_streamlit():
    if 'streamlit' not in sys.argv:

        sys.argv = [
            'streamlit',
            'run',
            resolver_path('main.py'),
            '--global.developmentMode=false'
        ]

        sys.exit(stcli.main())

if __name__ == '__main__':
    iniciar_streamlit()
