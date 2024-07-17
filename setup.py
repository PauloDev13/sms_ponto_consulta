import streamlit
import streamlit as st
import streamlit.web.cli as stcli
import streamlit.runtime.scriptrunner.magic_funcs

import pandas
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

import dotenv
from dotenv import load_dotenv

from bs4 import BeautifulSoup

from time import sleep
import xlsxwriter
import lxml
import openpyxl
import html5lib
import os, sys

import datetime
import locale
import calendar
from io import StringIO

from services import authenticate
from utils import utils
from utils import extractor_data

import logging

# Configurando logs
logging.basicConfig(level=logging.DEBUG, filename="setup.log", filemode='w')
logging.debug("Iniciando setup.py")


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
