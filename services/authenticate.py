# arquivo: login.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

import streamlit as st
import os
from time import sleep
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# URL do site
url_login = os.getenv("URL_BASE")

# Obtém as credenciais do arquivo .env
username = os.getenv("USER")
password = os.getenv("PASSWORD")


def login():
    # Configuração do WebDriver
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url_login)

        # Verfica se os campos de login e senha já foram carregados
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//*[@id='cpf']"))
        )
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//*[@id='senha']"))
        )

        sleep(2)
        driver.find_element(By.XPATH, "//*[@id='cpf']").send_keys(username)
        sleep(2)
        driver.find_element(By.XPATH, "//*[@id='senha']").send_keys(password)

        # Localiza o primeiro Iframe da página e entra nele
        driver.switch_to.frame(0)
        sleep(2)
        # Localiza dentro Iframe o elemento que tem o box do recaptcha e clica nele
        driver.find_element(by=By.XPATH, value="//*[@id='recaptcha-anchor']").click()
        # cap.click()
        # Sai do Iframe e volta para o html principal
        driver.switch_to.default_content()

        # Espera 30 segundos
        sleep(60)

        # Clique no botão de login
        button_login = driver.find_element(by=By.XPATH, value="//*[@id='form']/input")
        button_login.click()

        # Aguarda até que a URL mude após o login
        WebDriverWait(driver, 10).until(ec.url_contains('https://natal.rn.gov.br/sms/ponto/interno/inicio.php'))
        success = st.success('Login feito com sucesso!')
        sleep(3)
        success.empty()
        return driver

    except TimeoutException:
        error = st.error('Erro ao fazer login. Verifique suas credenciais.')
        sleep(3)
        error.empty()
        return None
    # finally:
    #     driver.quit()
