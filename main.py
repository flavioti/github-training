import argparse
import logging
import os
import time
from datetime import datetime
from functools import reduce

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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


class DerivBot:
    def __init__(self, conta: str) -> None:
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, timeout=10, ignored_exceptions=[])
        self.conta = conta

    def faz_tudo(
        self,
        action: str,  # clicar, digitar ou ler
        id: str = None,
        clazz: str = None,
        xpath: str = None,
        description: str = None,
        texto: str = None,
    ):
        max_tentativas = 50  # Máximo de tentativas
        contagem_tentativas = 0  # Guarda a quantidade de tentativas
        while contagem_tentativas < max_tentativas:
            contagem_tentativas += 1  # Incrementa o numero de tentativas
            try:
                if description:
                    logger.info(description)
                if id:
                    element = self.wait.until(EC.presence_of_element_located((By.ID, id)))
                elif clazz:
                    element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, clazz)))
                elif xpath:
                    element: WebElement = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                else:
                    raise Exception("Not id or clazz or xpath")

                if action == "clicar":
                    return element.click()
                elif action == "digitar" and texto:
                    for a in [1, 1, 1, 1, 1, 1, 1]:
                        element.send_keys(Keys.BACKSPACE)
                    time.sleep(1)
                    return element.send_keys(texto)
                elif action == "ler":
                    return element.text
                else:
                    raise Exception("Ação não definida, deve ser clicar ou digitar")
            except Exception as exc:
                # Caso der erro, ignora e tenta mais uma vez
                logger.error(f"Erro na tentativa #{contagem_tentativas} ao ler {description}")
                if contagem_tentativas >= max_tentativas:
                    raise exc
                time.sleep(0.5)

    def run(self):
        # Faz com que o driver sempre tente até 2 segundos carregar um objeto da página
        # O padrão é não esperar, tenta uma vez e se não encontrar dá erro
        # Configuração implícita global, serve para o restante do código
        self.driver.implicitly_wait(5)
        self.driver.get("https://www.deriv.com")

        # Clica no botão de login do site
        self.faz_tudo(
            action="clicar",
            id="dm-nav-login-button",
            description="Clicando no botão de login",
        )

        # Encontra o campo de email
        self.faz_tudo(
            action="digitar",
            texto=username,
            id="txtEmail",
            description="Digitando usuário",
        )

        # Encontrar o campo de senha
        self.faz_tudo(
            action="digitar",
            texto=password,
            id="txtPass",
            description="Digitando a senha",
        )

        # Encontrar botão conectar-se
        self.faz_tudo(action="clicar", clazz="button.button.secondary")

        # Aumentar o tamanho da tela
        self.driver.maximize_window()

        # ###### fim tela de login #######

        # Encontrar checkbox na tela de aviso após o login
        self.faz_tudo(
            action="clicar",
            clazz="warning-scam-message__checkbox-container--checkbox",
            description="Marcar checkbox na tela modal após o login",
        )

        # Encontrar botao para fechar tela de aviso
        self.faz_tudo(
            action="clicar",
            xpath='//*[@id="warning_scam_message_modal"]/div/div/button',
            description="Fechar tela modal após o login",
        )

        logger.info("Recarregando página para garantir que seja carregada")
        self.driver.refresh
        time.sleep(5)

        # ###### Escolher a conta de demonstração (DEMO)

        if args.conta.lower() == "demo":
            logger.info("Configurando conta DEMO")

            # Clica no botão para escolher conta
            self.faz_tudo(
                action="clicar",
                id="dt_core_account-info_acc-info",
                description="Escolher conta",
            )

            # Clica na aba da janelinha
            self.faz_tudo(
                action="clicar",
                id="dt_core_account-switcher_demo-tab",
                description="Clicar na aba após conta",
            )

            # Clica na conta demo
            self.faz_tudo(
                action="clicar",
                xpath=demo,
                description="Escolher conta de demonstração",
            )
            # ###### fim da configuração da conta demo
        elif args.conta.lower() == "real":
            logger.info("Configurando conta REAL")
        else:
            raise Exception("Conta demo ou real não definida")

        time.sleep(3)
        self.faz_tudo(
            action="clicar",
            clazz="cq-symbol-select-btn",
            description="Escolhendo tipo de jogo",
        )

        # sintetico
        time.sleep(3)  # Para funcionar no laptop do Flávio
        self.faz_tudo(
            action="clicar",
            xpath='//*[@id="trade"]/div/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div[2]/div/div[3]/div[2]',
        )

        # Clica no volatilidade 100
        time.sleep(3)
        self.faz_tudo(
            action="clicar",
            xpath='//*[@id="trade"]/div/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[4]/div[1]/div[11]',
            description="Escolher volatilidade 100",
        )
        # Igual\diferente
        time.sleep(1)
        self.faz_tudo(
            action="clicar",
            xpath='//*[@id="dt_contract_dropdown"]/div[1]',
            description="Click on Matches/Differs (1)",
        )

        # valor da aposta
        self.faz_tudo(action="digitar", id="dt_amount_input", texto="1")

        time.sleep(2)
        element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dt_contract_match_diff_item"]')))
        try:
            ActionChains(self.driver).scroll_to_element(element).perform()
        except Exception:
            pass
        time.sleep(2)
        element.click()

        self.faz_tudo(
            action="clicar",
            xpath='//*[@id="trade_container"]/div[4]/div/fieldset[2]/div[2]/label/div[1]/span[1]',
            description="Escolhe match/differ",
        )

        barra_de_numeros: WebElement = self.driver.find_element(
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

        element_num = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cq-current-price")))

        preco_anterior = None

        pred_0 = self.driver.find_element(
            by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[1]/span[1]'
        )
        pred_1 = self.driver.find_element(
            by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[1]/span[2]'
        )
        pred_2 = self.driver.find_element(
            by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[1]/span[3]'
        )
        pred_3 = self.driver.find_element(
            by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[1]/span[4]'
        )
        pred_4 = self.driver.find_element(
            by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[1]/span[5]'
        )
        pred_5 = self.driver.find_element(
            by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[2]/span[1]'
        )
        pred_6 = self.driver.find_element(
            by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[2]/span[2]'
        )
        pred_7 = self.driver.find_element(
            by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[2]/span[3]'
        )
        pred_8 = self.driver.find_element(
            by=By.XPATH, value='//*[@id="trade_container"]/div[4]/div/fieldset[3]/div[2]/div[2]/span[4]'
        )
        pred_9 = self.driver.find_element(
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

        state = {
            "counter": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "prob": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        }

        # Código abaixo roda eternamente para manter a tela aberta após terminar a configuração
        entrada_anterior = "?"
        menor_anterior = "?"
        data_hora_inicial = datetime.now()

        while True:
            position = "Pass"
            preco_atual = element_num.text
            digito_atual = preco_atual.strip()[-1:]
            n0, n1, n2, n3, n4, n5, n6, n7, n8, n9 = ler_percentuais()
            alist = [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9]
            menor_atual = alist.index(min(alist))  # Pega o menor numero

            # Somente troca o prediction se digito for novo (diferente)
            # if menor_atual != menor_anterior:
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
            if (
                preco_atual != preco_anterior
                and str(digito_atual) == str(menor_atual)
                and digito_atual != entrada_anterior
            ):
                apostar = True
                self.driver.find_element(by=By.ID, value="dt_purchase_digitdiff_button").click()

                # Espera 5 segundos para que o resultado apareça
                time.sleep(10)

                try:
                    # Captura texto do resultado da jogada Won or Lost
                    results = self.driver.find_elements(by=By.CLASS_NAME, value="dc-result__caption")
                    position = results[0].text
                except Exception:
                    logger.info("Erro ao tentar obter resultado")

                entrada_anterior = digito_atual
                menor_anterior = menor_atual

            tempo_decorrido = datetime.now() - data_hora_inicial

            if preco_atual != preco_anterior:
                # Contador de numeros para calcular a probabilidade
                #      Lista          digito atual      soma mais hum
                state["counter"][int(digito_atual)] += 1
                state["sum"] = reduce(lambda x, y: x + y, state["counter"])

                for n in range(0, 10):
                    c = state["counter"][n]
                    summ = state["sum"]
                    state["prob"][n] = "{:.1f}".format((c / summ) * 100)

                logger.info(
                    f"{preco_atual.ljust(8, ' ')} "
                    # + f"{str(n0).ljust(4, ' ')} "
                    # + f"{str(n1).ljust(4, ' ')} "
                    # + f"{str(n2).ljust(4, ' ')} "
                    # + f"{str(n3).ljust(4, ' ')} "
                    # + f"{str(n4).ljust(4, ' ')} "
                    # + f"{str(n5).ljust(4, ' ')} "
                    # + f"{str(n6).ljust(4, ' ')} "
                    # + f"{str(n7).ljust(4, ' ')} "
                    # + f"{str(n8).ljust(4, ' ')} "
                    # + f"{str(n9).ljust(4, ' ')} "
                    # + f"menor {menor_perc} "
                    + f"menor {menor_atual} "
                    + f"digito {digito_atual} "
                    + f"entrada_anterior {entrada_anterior} "
                    + f"apostar {apostar} "
                    + f"result {position} "
                    + "uptime "
                    + "{:.2f}".format(tempo_decorrido.total_seconds() / 60)
                )

                if not os.path.exists("log.csv"):
                    with open("log.csv", "a") as myfile:
                        myfile.write(
                            "data_hora;price;n0;n1;n2;n3;n4;n5;n6;n7;n8;n9;menor_atual;digito_atual;"
                            + "entrada_anterior;apostar;position;uptime;c0;c1;c2;c3;c4;c5;c6;c7;c8;"
                            + "c9;p0;p1;p2;p3;p4;p5;p6;p7;p8;p9;saldo"
                            + "\n"
                        )

                saldo = self.driver.find_element(by=By.CLASS_NAME, value="acc-info__balance")

                with open("log.csv", "a") as myfile:
                    myfile.write(
                        ";".join(
                            [
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                preco_atual,
                                str(n0),
                                str(n1),
                                str(n2),
                                str(n3),
                                str(n4),
                                str(n5),
                                str(n6),
                                str(n7),
                                str(n8),
                                str(n9),
                                str(menor_atual),
                                digito_atual,
                                entrada_anterior,
                                str(apostar),
                                position,
                                "{:.2f}".format(tempo_decorrido.total_seconds() / 60),
                            ]
                            + [str(n) for n in state["counter"]]
                            + [str(n) for n in state["prob"]]
                            + [saldo.text[0:5].strip()]
                        ).replace(".", ",")
                        + "\n"
                    )

            if tempo_decorrido.total_seconds() >= 1800:  # 30 * 60
                logger.info("Trinta minutos se passaram, recarregando página")
                self.driver.refresh
                time.sleep(10)
                data_hora_inicial = datetime.now()

            preco_anterior = preco_atual


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--conta", required=False, default="real")
    args = parser.parse_args()

    while True:
        try:
            DerivBot(args.conta.lower()).run()
            time.sleep(10)
        except Exception as exc:
            logger.exception(exc)
            continue
