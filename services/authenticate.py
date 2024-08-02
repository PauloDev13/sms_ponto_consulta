from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchWindowException,
    ElementClickInterceptedException)
from selenium.webdriver.support import expected_conditions as ec

import os, sys
import streamlit as st
from time import sleep
from dotenv import load_dotenv

from utils import utils

# Carrega o arquivo .env
load_dotenv()

# Atribuições das variáveis declaradas no .env
url_login = os.getenv("URL_BASE")
url_init = os.getenv("URL_INIT")
username = os.getenv("USER")
password = os.getenv("PASSWORD")


# FUNÇÃO LOGIN
def login():
    # Configuração do WebDriver
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    try:
        # Acessa a URL que exibe a página de login
        driver.get(url_login)

        # Verifica se a página HTML carregou os campos de login e senha
        load_login = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//*[@id='cpf']"))
        )
        load_senha = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//*[@id='senha']"))
        )

        if load_login and load_senha:
            # Acessa o campo de login, insere o login, espera 1 segundo, acessa o campo senha e insere a senha
            driver.find_element(By.XPATH, '//*[@id="cpf"]').send_keys(username)
            sleep(1)
            driver.find_element(By.XPATH, "//*[@id='senha']").send_keys(password)
        else:
            utils.default_msg('Erro ao identificar TAGs de login', 'error')
            st.stop()

        # Localiza o primeiro Iframe da página, entra nele, espera 1 segundo
        # Localiza dentro Iframe o elemento o box do recaptcha e clica
        # Sai do Iframe e volta para o html principal
        # Espera 30 segundos para que o usuário digite o captcha, se aparecer
        driver.switch_to.frame(0)
        driver.find_element(by=By.XPATH, value="//*[@id='recaptcha-anchor']").click()
        driver.switch_to.default_content()
        sleep(60)

        # Localiza o botão de login e clica
        button_login = driver.find_element(by=By.XPATH, value="//*[@id='form']/input")
        button_login.click()

        sleep(1)
        # Checa se a URL da página inicial foi carregada no navegador
        load_page = WebDriverWait(driver, 10).until(
            ec.url_contains(url_init)
        )

        # Se a página inicial carregou, exibe mensagem de sucesso
        # Se não, exibe mensagem de alerta
        if load_page:
            utils.default_msg('Login realizado com sucesso!', 'success')

        else:
            utils.default_msg('Falha no login! Tente novamente.', 'info')

        # Retorna uma instância do navegador.
        return driver

    # Se ocorrer erros no processo de login exibe mensagens
    except ElementClickInterceptedException as e:
        utils.default_msg('Erro ao clicar num elemento da página! Tente novamente', 'error')
        print(f'Erro stacktrace: {e}')
        logout()
        return None
    except TimeoutException as ex:
        utils.default_msg('A pagina demorou a responder! Tente novamente', 'error')
        print(f'Erro stacktrace: {ex}')
        logout()
        return None

    except NoSuchWindowException as ex_:
        utils.default_msg('Falha no login! Tente novamente', 'error')
        print(f'Erro stacktrace: {ex_}')
        logout()
        return None


# FUNÇÃO LOGOUT
def logout():
    # Se houver uma sessão ativa, encerra a cessão, deleta a sessão do estado (state),
    # exibe mensagem de sucesso, espera 3 segundos e fecha a mensagem
    if 'driver' in st.session_state:
        st.session_state.driver.quit()
        del st.session_state.driver
        utils.default_msg('Aplicação encerrada!', 'info')
        sys.exit()
