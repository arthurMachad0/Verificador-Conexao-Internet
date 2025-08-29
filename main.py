import flet as ft
import time
import pandas as pd
import os
import requests
from datetime import datetime
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import (
    TimeoutException,
    ElementNotInteractableException,
    NoSuchElementException
)
import urllib.request
import openpyxl

XPATH_DOWNLOAD = '//span[@class="result-data-large number result-data-value download-speed"]'
XPATH_UPLOAD = '//span[@class="result-data-large number result-data-value upload-speed"]'
XPATH_PING = '//span[@class="result-data-value ping-speed"]'
ID_ACEITAR = 'onetrust-accept-btn-handler'
CLASS_START_BTN = 'start-text'
XPATH_RESULTADOS_DIV = '//div[@data-result-id]'
CLASS_BOTAO_FECHAR_AVISO = 'close-btn'

class INTERNET:
    def __init__(self, headless=False) -> None:
        self.base_url = "https://www.speedtest.net/pt"
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        
        if headless:
            options.add_argument("--headless")  # Modo headless
            options.add_argument("--disable-gpu")  # Desabilita GPU para headless
        
        try:
            service = Service(ChromeDriverManager().install())
        except ValueError:
            latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
            latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode("utf-8")
            service = Service(ChromeDriverManager(latest_chromedriver_version).install())

        self.browser = Chrome(service=service, options=options)
        self.browser.get(self.base_url)
        
        time.sleep(3)
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.ID, ID_ACEITAR))
        ).click()

        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, CLASS_START_BTN))
        ).click()
        print("Teste iniciado. Aguardando resultados...")

        time.sleep(3)
        self._fechar_aviso_se_existir()

        WebDriverWait(self.browser, 90).until(
            EC.presence_of_element_located((By.XPATH, XPATH_RESULTADOS_DIV))
        )
        print("Resultados carregados.")

        time.sleep(3)
        self._fechar_aviso_se_existir()
        self.browser.execute_script("window.scrollTo(0, 0);")

    def _fechar_aviso_se_existir(self):
        """
        Verifica a presença do modal de aviso. Se encontrá-lo, espera o botão ser clicável e o fecha.
        """
        try:
            xpath_aviso_texto = '//*[contains(text(), "Voltar aos resultados do teste")]'
            WebDriverWait(self.browser, 3).until(
                EC.presence_of_element_located((By.XPATH, xpath_aviso_texto))
            )
            print("Aviso 'Voltar aos resultados do teste' detectado.")
            
            time.sleep(10)
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # --- MODIFICAÇÃO PRINCIPAL ---
            # Espera até que o botão de fechar esteja realmente pronto para ser clicado
            print("Aguardando o botão de fechar ser interativo...")
            botao_fechar = WebDriverWait(self.browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[2]/div/div[4]/div/div[8]/div/div/div[2]/a'))
            )
            
            botao_fechar.click()
            print("Aviso fechado com sucesso.")
            time.sleep(1)
            self.browser.execute_script("window.scrollTo(0, 0);")
            
        except TimeoutException:
            print("Nenhum aviso de aplicativo foi exibido.")
            pass
        except ElementNotInteractableException:
            print("ERRO: O botão de fechar foi encontrado mas não é interativo. Tentando clicar com JavaScript...")
            
            try:
                botao_fechar = self.browser.find_element(By.XPATH, '//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[2]/div/div[4]/div/div[8]/div/div/div[2]/a')
                self.browser.execute_script("arguments[0].click();", botao_fechar)
                print("Aviso fechado com sucesso via JavaScript.")
            except Exception as e:
                print(f"Falha ao tentar clicar com JavaScript: {e}")

    def data_e_hora(self):
        """Obtém a data e hora local da máquina. Mais robusto e sem dependências externas."""
        agora = datetime.now()
        return agora.strftime('%d/%m/%Y'), agora.strftime('%H:%M:%S')

    def extract_data(self):
        print("Extraindo dados do teste...")
        download = self.browser.find_element(By.XPATH, XPATH_DOWNLOAD).text
        upload = self.browser.find_element(By.XPATH, XPATH_UPLOAD).text
        ping = self.browser.find_element(By.XPATH, XPATH_PING).text

        data, hora = self.data_e_hora()

        self.info = []
        info_extraida = {
            'Data': data,
            'Hora': hora,
            'Download (Mbps)': download,
            'Upload (Mbps)': upload,
            'Ping (ms)': ping,
        }
        self.info.append(info_extraida)

        tabela_temporaria = pd.DataFrame(self.info)
        print("Dados extraídos:")
        print(tabela_temporaria)
        return self.info

def main(page: ft.Page):
    page.title = "Teste Automatizado de Internet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    result_text = ft.Text(value="Clique em 'Começar' para iniciar o teste de internet.", size=20)
    result_display = ft.Column()

    run_in_background = ft.Checkbox(label="Rodar em Segundo Plano", value=False)

    def start_test(e):
        result_display.controls.clear()  # Limpa resultados anteriores
        result_text.value = "Executando teste de internet..."
        page.update()

        # Verifica se o checkbox está marcado para rodar em modo headless
        headless = run_in_background.value

        internet = INTERNET(headless=headless)
        resultados = internet.extract_data()

        # Exibe os resultados na interface
        if resultados and isinstance(resultados, list) and len(resultados) > 0:
            for chave, valor in resultados[0].items():
                result_display.controls.append(ft.Text(f"{chave}: {valor}", size=16))
        else:
            result_display.controls.append(ft.Text("Nenhum resultado encontrado.", size=16))

        result_text.value = "Teste concluído!"
        page.update()

        novos_dados = pd.DataFrame(resultados)
        nome_arquivo = "informacoes.xlsx"
        if os.path.exists(nome_arquivo):
            print(f"Adicionando dados ao arquivo existente: {nome_arquivo}")
            df_existente = pd.read_excel(nome_arquivo)
            df_final = pd.concat([df_existente, novos_dados], ignore_index=True)
        else:
            print(f"Criando novo arquivo: {nome_arquivo}")
            df_final = novos_dados

        df_final.to_excel(nome_arquivo, index=False)
        print("Dados salvos com sucesso!")

    start_button = ft.ElevatedButton(text="Começar", on_click=start_test)

    page.add(
        ft.Column(
            [
                ft.Text(value="Teste Automatizado de Internet", size=30, weight=ft.FontWeight.BOLD),
                result_text,
                ft.Text(value="Opção Extra", size=20, weight=ft.FontWeight.BOLD),
                
                ft.Row(
                    [run_in_background],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                start_button,
                result_display
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)

