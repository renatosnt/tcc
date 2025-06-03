from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# === Configuração do navegador e pasta de download ===
download_dir = os.path.abspath("downloads_cnpq")
os.makedirs(download_dir, exist_ok=True)

options = Options()
options.add_argument("--headless")
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver = webdriver.Chrome(options=options)

try:
    driver.get("https://dgp.cnpq.br/dgp/faces/consulta/consulta_parametrizada.jsf")

    # Espera até que o campo de estado esteja presente
    wait = WebDriverWait(driver, 30)
    select_estado = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="formBusca:estado"]')))
    time.sleep(1)

    # Seleciona MG
    for option in select_estado.find_elements(By.TAG_NAME, 'option'):
        if "MG" in option.text:
            option.click()
            break

    # Clica em Buscar
    btn_consultar = wait.until(EC.element_to_be_clickable((By.ID, "formBusca:buscar")))
    btn_consultar.click()
    time.sleep(10)

    # Clica no botão de exportar CSV (ID pode mudar, vamos tentar por texto ou posição)
    export_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Gerar arquivo para download"]')))
    export_btn.click()
    print("⏬ Gerando e baixando CSV...")

    time.sleep(15)  # tempo para download

finally:
    driver.quit()

print(f"✅ Arquivo baixado para: {download_dir}")
