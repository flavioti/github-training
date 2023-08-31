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
            time.sleep(0.5)


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

time.sleep(3)
faz_tudo(
    action="clicar",
    clazz="cq-symbol-select-btn",
    description="Escolhendo tipo de jogo",
)

# sintetico
time.sleep(3)  # Para funcionar no laptop do Flávio
faz_tudo(
    action="clicar",
    xpath='//*[@id="trade"]/div/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div[2]/div/div[3]/div[2]',
)

# Clica no volatilidade 100
time.sleep(3)
faz_tudo(
    action="clicar",
    xpath='//*[@id="trade"]/div/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[4]/div[1]/div[11]',
    # clazz='sc-mcd__item--R_100 '
    description="Escolher volatilidade 100",
)
# Igual\diferente
time.sleep(1)
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

pred_0 = driver.find_element(
    by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[1]/span[1]'
)
pred_1 = driver.find_element(
    by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[1]/span[2]'
)
pred_2 = driver.find_element(
    by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[1]/span[3]'
)
pred_3 = driver.find_element(
    by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[1]/span[4]'
)
pred_4 = driver.find_element(
    by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[1]/span[5]'
)
pred_5 = driver.find_element(
    by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[2]/span[1]'
)
pred_6 = driver.find_element(
    by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[2]/span[2]'
)
pred_7 = driver.find_element(
    by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[2]/span[3]'
)
pred_8 = driver.find_element(
    by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[2]/span[4]'
)
pred_9 = driver.find_element(
    by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[2]/span[5]'
)


def ler_percentuais():
    try:
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
        return n0, n1, n2, n3, n4, n5, n6, n7, n8, n9
    except Exception:
        return 0, 0, 0, 0, 0, 0, 0, 0, 0, 0


# Código abaixo roda eternamente para manter a tela aberta após terminar a configuração
# Caso o navegador seja fechado, o código também será encerrado
navegador_aberto = True
entrada_anterior = "?"
menor_anterior = "?"
while navegador_aberto:
    try:
        preco_atual = element_num.text
        digito_atual = preco_atual.strip()[-1:]
        n0, n1, n2, n3, n4, n5, n6, n7, n8, n9 = ler_percentuais()
        alist = [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9]

        # TODO: As vezes tem dois numero com porcentagens baixas e iguais, nesse caso aborta (não joga)
        menor_atual = alist.index(min(alist))  # Pega o menor numero

        # Somente troca o prediction se digito for novo (diferente)
        if menor_atual != menor_anterior:
            if menor_atual == 0:
                pred_0.click()
            elif menor_atual == 1:
                pred_1.click()
            elif menor_atual == 2:
                pred_2.click()
            elif menor_atual == 3:
                pred_3.click()
            elif menor_atual == 4:
                pred_4.click()
            elif menor_atual == 5:
                pred_5.click()
            elif menor_atual == 6:
                pred_6.click()
            elif menor_atual == 7:
                pred_7.click()
            elif menor_atual == 8:
                pred_8.click()
            elif menor_atual == 9:
                pred_9.click()

        apostar = False
        if preco_atual != preco_anterior and str(digito_atual) == str(menor_atual) and digito_atual != entrada_anterior:
            apostar = True
            driver.find_element(by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[2]/div[2]/label/div[1]/span[1]').click()

            entrada_anterior = digito_atual
            menor_anterior = menor_atual

        if preco_atual != preco_anterior:
            logger.info(
                f"{preco_atual.ljust(8, ' ')} "
                + f"{str(n0).ljust(4, ' ')} "
                + f"{str(n1).ljust(4, ' ')} "
                + f"{str(n2).ljust(4, ' ')} "
                + f"{str(n3).ljust(4, ' ')} "
                + f"{str(n4).ljust(4, ' ')} "
                + f"{str(n5).ljust(4, ' ')} "
                + f"{str(n6).ljust(4, ' ')} "
                + f"{str(n7).ljust(4, ' ')} "
                + f"{str(n8).ljust(4, ' ')} "
                + f"{str(n9).ljust(4, ' ')} "
                # + f"menor {menor_perc} "
                + f"menor {menor_atual} "
                + f"digito {digito_atual} "
                + f"entrada_anterior {entrada_anterior} "
                + f"apostar {apostar} "
            )

        preco_anterior = preco_atual

    except Exception:
        pass

logger.info("finalizado")
