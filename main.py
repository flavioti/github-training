import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

user = os.environ["user"]
password = os.environ["password"]

driver = webdriver.Chrome()

# Faz com que o driver sempre tente até 2 segundos carregar um objeto da página
# O padrão é não esperar, tenta uma vez e se não encontrar dá erro
# Configuração implícita global, serve para o restante do código
seconds_to_wait = 2
driver.implicitly_wait(seconds_to_wait)


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
senha = driver.find_element(by=By.ID, value="txtPass")
senha.send_keys(password)

# Encontrar botão conectar-se
entrar = driver.find_element(By.CLASS_NAME, "button.button.secondary")

# Clicar no botão conectar-se
entrar.click()

# Aumentar o tamanho da tela
driver.maximize_window()


print("finalizado")
