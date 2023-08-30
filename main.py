import logging
import os
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

username = os.environ["user"]
password = os.environ["password"]
demo = os.environ["demo"]


def faz_tudo(
    action: str,  # clicar, digitar ou ler
    id: str = None,
    clazz: str = None,
    xpath: str = None,
    description: str = None,
    texto: str = None,
):
    time.sleep(0.5)
    max_tentativas = 50  # Máximo de tentativas
    contagem_tentativas = 0  # Guarda a quantidade de tentativas
    terminado = False  # Guarda informação se conseguiu clicar ou não no elemento
    while contagem_tentativas < max_tentativas and not terminado:
        contagem_tentativas += 1  # Incrementa o numero de tentativas
        try:
            if description:
                logger.info(description)
            if id:
                element = wait.until(EC.presence_of_element_located((By.ID, id)))
            elif clazz:
                element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, clazz)))
            elif xpath:
                element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            else:
                raise Exception("Not id or clazz or xpath")

            if action == "clicar":
                return element.click()
            elif action == "digitar" and texto:
                return element.send_keys(texto)
            elif action == "ler":
                return element.text
            else:
                raise Exception("Ação não definida, deve ser clicar ou digitar")
            terminado = True
        except Exception as exc:
            # Caso der erro, ignora e tenta mais uma vez
            logger.error(f"Erro na tentativa #{contagem_tentativas} ao ler {description}")
            if contagem_tentativas >= max_tentativas:
                raise exc


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
faz_tudo(
    action="clicar",
    id="dm-nav-login-button",
    description="Clicando no botão de login",
)

# Encontra o campo de email
faz_tudo(
    action="digitar",
    texto=username,
    id="txtEmail",
    description="Digitando usuário",
)

# Encontrar o campo de senha
faz_tudo(
    action="digitar",
    texto=password,
    id="txtPass",
    description="Digitando a senha",
)

# Encontrar botão conectar-se
faz_tudo(action="clicar", clazz="button.button.secondary")

# Aumentar o tamanho da tela
driver.maximize_window()

# ###### fim tela de login #######

# Encontrar checkbox na tela de aviso após o login
faz_tudo(
    action="clicar",
    clazz="warning-scam-message__checkbox-container--checkbox",
    description="Marcar checkbox na tela modal após o login",
)

# Encontrar botao para fechar tela de aviso
faz_tudo(
    action="clicar",
    xpath='//*[@id="warning_scam_message_modal"]/div/div/button',
    description="Fechar tela modal após o login",
)


# ###### Escolher a conta de demonstração (DEMO)

# Clica no botão para escolher conta
faz_tudo(
    action="clicar",
    id="dt_core_account-info_acc-info",
    description="Escolher conta",
)

# Clica na aba da janelinha
faz_tudo(
    action="clicar",
    id="dt_core_account-switcher_demo-tab",
    description="Clicar na aba após conta",
)

# Clica na conta demo
faz_tudo(
    action="clicar",
    xpath=demo,
    description="Escolher conta de demonstração",
)
# ###### fim da configuração da conta demo

faz_tudo(
    action="clicar",
    clazz="cq-symbol-select-btn",
    description="Escolhendo tipo de jogo",
)

# sintetico
faz_tudo(
    action="clicar",
    xpath='//*[@id="trade"]/div/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div[2]/div/div[3]/div[2]',
)

# Clica no volatilidade 100
faz_tudo(
    action="clicar",
    xpath='//*[@id="trade"]/div/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[4]/div[1]/div[11]',
    # clazz='sc-mcd__item--R_100 '
    description="Escolher volatilidade 100",
)
# Igual\diferente
faz_tudo(
    action="clicar",
    xpath='//*[@id="dt_contract_dropdown"]/div[1]',
    description="Click on Matches/Differs (1)",
)


time.sleep(2)
element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dt_contract_match_diff_item"]')))
try:
    ActionChains(driver).scroll_to_element(element).perform()
except Exception:
    pass
time.sleep(2)
element.click()


faz_tudo(
    action="clicar",
    xpath='//*[@id="trade_container"]/div[4]/div/fieldset[2]/div[2]/label/div[1]/span[1]',
    description="Escolhe match/differ",
)

barra_de_numeros: WebElement = driver.find_element(
    by=By.XPATH, value='//*[@id="trade"]/div/div[1]/div/div/div[1]/div[5]/div/div/div[2]'
)

ele00 = barra_de_numeros.find_elements(by=By.TAG_NAME, value="div")[0]
ele02 = barra_de_numeros.find_elements(by=By.TAG_NAME, value="div")[2]
ele04 = barra_de_numeros.find_elements(by=By.TAG_NAME, value="div")[4]
ele06 = barra_de_numeros.find_elements(by=By.TAG_NAME, value="div")[6]
ele08 = barra_de_numeros.find_elements(by=By.TAG_NAME, value="div")[8]
ele10 = barra_de_numeros.find_elements(by=By.TAG_NAME, value="div")[10]
ele12 = barra_de_numeros.find_elements(by=By.TAG_NAME, value="div")[12]
ele14 = barra_de_numeros.find_elements(by=By.TAG_NAME, value="div")[14]
ele16 = barra_de_numeros.find_elements(by=By.TAG_NAME, value="div")[16]
ele18 = barra_de_numeros.find_elements(by=By.TAG_NAME, value="div")[18]

element_num = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cq-current-price")))

preco_anterior = None

# Código abaixo roda eternamente para manter a tela aberta após terminar a configuração
# Caso o navegador seja fechado, o código também será encerrado
navegador_aberto = True
while navegador_aberto:
    # numero_atual = espera_e_clica(
    #     action="ler",
    #     clazz="cq-current-price",
    #     description="Numero atual",
    # )

    preco_atual = element_num.text.ljust(8, " ")

    digito = preco_atual.strip()[-1:]

    if preco_atual != preco_anterior:
        n0 = float(ele00.text.replace("0\n", "").replace("%", ""))
        n1 = float(ele02.text.replace("1\n", "").replace("%", ""))
        n2 = float(ele04.text.replace("2\n", "").replace("%", ""))
        n3 = float(ele06.text.replace("3\n", "").replace("%", ""))
        n4 = float(ele08.text.replace("4\n", "").replace("%", ""))
        n5 = float(ele10.text.replace("5\n", "").replace("%", ""))
        n6 = float(ele12.text.replace("6\n", "").replace("%", ""))
        n7 = float(ele14.text.replace("7\n", "").replace("%", ""))
        n8 = float(ele16.text.replace("8\n", "").replace("%", ""))
        n9 = float(ele18.text.replace("9\n", "").replace("%", ""))

        alist = [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9]

        menor_perc = min(alist)
        menor_idx = alist.index(min(alist))

        if str(digito) == str(menor_idx):
            apostar = "yes"

            # APOSTAR AQUI

        else:
            apostar = "no"

        logger.info(
            f"{preco_atual} "
            + f"{str(n0).ljust(6, ' ')} "
            + f"{str(n1).ljust(6, ' ')} "
            + f"{str(n2).ljust(6, ' ')} "
            + f"{str(n3).ljust(6, ' ')} "
            + f"{str(n4).ljust(6, ' ')} "
            + f"{str(n5).ljust(6, ' ')} "
            + f"{str(n6).ljust(6, ' ')} "
            + f"{str(n7).ljust(6, ' ')} "
            + f"{str(n8).ljust(6, ' ')} "
            + f"{str(n9).ljust(6, ' ')} "
            + f" menor {menor_perc} "
            + f" idx {menor_idx} "
            + f" digito {digito}"
            + f" apostar {apostar}"
        )

        preco_anterior = preco_atual


logger.info("finalizado")
