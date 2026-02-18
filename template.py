import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("...")
driver.maximize_window() # Agrandir la fenêtre


# Écrire dans un champ
element = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH,"//*[@id='search']"))
)
element.send_key("Dune")


# Appuyer sur une touche
element = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH,"//*[@id='search']"))
)
element.send_keys(Keys.ENTER)


# Cliquer
element = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.ID, "icon-search"))
    )
element.click()


# Rechercher un élément
# Par ID
element = EC.presence_of_element_located(By.ID, "mon_id")

# Par nom
element = EC.presence_of_element_located(By.NAME, "username")

# Par classe
element = EC.presence_of_element_located(By.CLASS_NAME, "btn-primary")

# Par CSS Selector
element = EC.presence_of_element_located(By.CSS_SELECTOR, "input[type='text']")

# Par XPath
element = EC.presence_of_element_located(By.XPATH, "//button[text()='Valider']")

# Attendre qu’un élément soit disponible
wait = WebDriverWait(driver, 10)

element = wait.until(
    EC.presence_of_element_located((By.ID, "mon_id"))
)


# Vérifier un résultat
assert "Bienvenue" in driver.page_source


driver.quit()