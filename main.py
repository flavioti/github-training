import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

user = os.environ["user"]
password = os.environ["password"]

driver = webdriver.Chrome()

driver.get("https://www.deriv.com")

time.sleep(5)

# Procura o botao de login na pagina e atribui a variabel chamada botao
botao = driver.find_element(by=By.ID, value="dm-nav-login-button")

# Clica no botão de login do site
botao.click()

time.sleep(5)

# Encontra o campo de email
email = driver.find_element(by=By.ID, value="txtEmail")
email.send_keys(user)

# Encontrar o campo de senha 
senha = driver.find_element(by= By.ID, value="txtPass")
senha.send_keys(password)

print("finalizado")
