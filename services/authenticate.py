# arquivo: login.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import os
from time import sleep
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# URL do site
url_login = os.getenv("URL_BASE")

# Obtém as credenciais do arquivo .env
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")


def login():
    # Configuração do WebDriver
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    try:
        # driver.get(url_login)
        driver.get('https://natal.rn.gov.br/sms/ponto/index.php')

        # Aguarde o carregamento da página de login
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="cpf"]'))
        )

        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="senha"]'))
        )

        driver.find_element(By.XPATH, '//*[@id="cpf"]').send_keys(username)
        # driver.find_element(By.XPATH, '//*[@id="senha"]').send_keys(password)

        # Espera 30 segundos
        sleep(30)

        # Clique no botão de login
        button_login = driver.find_element(by=By.XPATH, value="//*[@id='form']/input")
        button_login.click()

        # Verifique se o login foi bem-sucedido
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, "grafico_grande"))
        )

        # Aguarda até que a URL mude após o login
        # WebDriverWait(driver, 10).until(ec.url_contains(url_login))
        WebDriverWait(driver, 10).until(ec.url_contains('https://natal.rn.gov.br/sms/ponto/index.php'))
        return True

    except TimeoutException:
        print("Erro ao fazer login. Verifique suas credenciais, URL e seletores.")
        return False
    finally:
        driver.quit()
