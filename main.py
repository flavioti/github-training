import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

user = os.environ["user"]
password = os.environ["password"]


def espera_e_clica(id: str = None, clazz: str = None, xpath: str = None):
    time.sleep(2)
    if id:
        element = wait.until(EC.presence_of_element_located((By.ID, id)))
    elif clazz:
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, clazz)))
    elif xpath:
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    else:
        raise Exception("Not id or clazz or xpath")
    element.click()


driver = webdriver.Chrome()

# Configuração explicita para ser usado ao buscar componentes
max_explicit_wait_seconds = 10
wait = WebDriverWait(driver, timeout=max_explicit_wait_seconds, ignored_exceptions=[])

# Faz com que o driver sempre tente até 2 segundos carregar um objeto da página
# O padrão é não esperar, tenta uma vez e se não encontrar dá erro
# Configuração implícita global, serve para o restante do código
seconds_to_wait = 5
driver.implicitly_wait(seconds_to_wait)


driver.get("https://www.deriv.com")


# Clica no botão de login do site
espera_e_clica(id="dm-nav-login-button")

# Encontra o campo de email
email = driver.find_element(by=By.ID, value="txtEmail")
wait.until(lambda d: email.is_displayed())
email.send_keys(user)

# Encontrar o campo de senha
senha = driver.find_element(by=By.ID, value="txtPass")
senha.send_keys(password)

# Encontrar botão conectar-se
espera_e_clica(clazz="button.button.secondary")

# Aumentar o tamanho da tela
driver.maximize_window()

# ###### fim tela de login #######

# Encontrar checkbox na tela de aviso após o login
espera_e_clica(clazz="warning-scam-message__checkbox-container--checkbox")

# Encontrar botao para fechar tela de aviso
scammer_warning_button_class = '//*[@id="warning_scam_message_modal"]/div/div/button'
scammer_warning_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, scammer_warning_button_class))
)
wait.until(lambda d: scammer_warning_button.is_enabled() and scammer_warning_button.is_displayed())
scammer_warning_button.click()

# ###### Escolher a conta de demonstração (DEMO)

# Clica no botão para escolher conta
espera_e_clica(id="dt_core_account-info_acc-info")

# Clica na aba da janelinha
espera_e_clica(id="dt_core_account-switcher_demo-tab")

# Clica na conta demo
espera_e_clica(id="dt_VRTC4693085")

# ###### fim da configuração da conta demo

espera_e_clica(clazz="cq-symbol-select-btn")

# sintetico
espera_e_clica(
    xpath='//*[@id="trade"]/div/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div[2]/div/div[3]/div[2]'
)

# Clica no volatilidade 100
espera_e_clica(
    xpath='//*[@id="trade"]/div/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[4]/div[1]/div[11]'
)

espera_e_clica(xpath='//*[@id="dt_contract_dropdown"]/div[1]')
espera_e_clica(id="dt_contract_match_diff_item")


espera_e_clica(xpath='//*[@id="trade_container"]/div[4]/div/fieldset[2]/div[2]/label/div[1]/span[1]')

# Código abaixo roda eternamente para manter a tela aberta após terminar a configuração
# Caso o navegador seja fechado, o código também será encerrado
navegador_aberto = True
while navegador_aberto:
    try:
        print(driver.current_url)
    except Exception:
        driver.quit()
        navegador_aberto = False
    time.sleep(2)


print("finalizado")
