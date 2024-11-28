import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


def fetch_academy_addresses(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if "Acads" in data:
            return data['Acads']
        else:
            raise ValueError("Resposta da API inválida. Campo 'Acads' não encontrado.")
    except Exception as e:
        print(f"Erro ao buscar endereços: {e}")
        return []


def pesquisar_no_google_maps(endereco_1):
    api_url = "http://127.0.0.1:5000/get_all_acads"
    academias = fetch_academy_addresses(api_url)

    if not academias:
        print("Nenhum endereço foi retornado pela API.")
        return []


    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    resultado_academias = []

    try:
        driver.get("https://www.google.com/maps")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchboxinput"))
        )

        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.send_keys(endereco_1)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button//div[contains(text(),'Rotas')]"))
        )

        rotas_button = driver.find_element(By.XPATH, "//button//div[contains(text(),'Rotas')]")
        rotas_button.click()
        time.sleep(3)

        for acad in academias:
            endereco_2 = acad['endereco']
            lotacao = acad['lotacao']


            destination_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tactile-searchbox-input"))
            )

            destination_box.click()
            destination_box.send_keys(Keys.CONTROL + "a")
            destination_box.send_keys(Keys.BACKSPACE)
            destination_box.send_keys(endereco_2)
            destination_box.send_keys(Keys.RETURN)
            time.sleep(3)

            try:
                tempo_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@aria-hidden='false']//span[contains(text(),'min')]"))
                )
                tempo = tempo_element.text

                tempo_min = int(tempo.split()[0])
                resultado = (tempo_min + lotacao) / 2

                resultado_academias.append({
                    'nome': acad['nome_fantasia'],
                    'endereco': endereco_2,
                    'resultado': resultado
                })
            except Exception as e:
                print(f"Erro ao processar o tempo para {endereco_2}: {e}")
                continue

    finally:
        driver.quit()

    if not resultado_academias:
        print("Nenhum resultado encontrado para as academias.")
    else:
        print(f"Total de resultados encontrados: {len(resultado_academias)}")

    resultado_academias.sort(key=lambda x: x['resultado'])

    return resultado_academias
