from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random


def pesquisar_no_google_maps():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    endereco_1 = "Joaquim Sá 20, Fortaleza"
    enderecos_fortaleza = [
        "Avenida Beira Mar, Fortaleza",
        "Rua dos Três Irmãos, Fortaleza",
        "Rua Dr. José Lourenço, Fortaleza",
        "Avenida Washington Soares, Fortaleza",
        "Rua Padre Valdevino, Fortaleza"
    ]

    print(f"Iniciando pesquisa de rotas a partir de: {endereco_1}\n")

    driver.get("https://www.google.com/maps")
    time.sleep(3)

    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.send_keys(endereco_1)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

    # Usando o texto "Rotas" para identificar o botão
    rotas_button = driver.find_element(By.XPATH, "//button//div[contains(text(),'Rotas')]")
    rotas_button.click()
    time.sleep(3)

    for endereco_2 in enderecos_fortaleza:
        print(f"\nPesquisando rota para: {endereco_2}")

        destination_box = driver.find_element(By.CLASS_NAME, "tactile-searchbox-input")
        destination_box.click()
        destination_box.send_keys(Keys.CONTROL + "a")
        destination_box.send_keys(Keys.BACKSPACE)
        time.sleep(1)

        destination_box.send_keys(endereco_2)
        destination_box.send_keys(Keys.RETURN)
        time.sleep(5)

        try:
            tempo_element = driver.find_element(By.XPATH, "//div[@aria-hidden='false']//span[contains(text(),'min')]")
            tempo = tempo_element.text
            print(f"Tempo estimado para {endereco_2}: {tempo}")
        except Exception as e:
            print(f"Não foi possível encontrar o tempo para {endereco_2}. Erro: {e}")

        time.sleep(2)

    driver.quit()

pesquisar_no_google_maps()
