from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://www.kickstarter.com/?lang=fr")
driver.maximize_window()

wait = WebDriverWait(driver, 15)

# Cliquer sur l'icône de recherche
bouton_recherche = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Search']"))
)
bouton_recherche.click()

# Champ de recherche
barre_recherche = wait.until(
    EC.presence_of_element_located((By.NAME, "term"))
)
barre_recherche.send_keys("justloui")
barre_recherche.send_keys(Keys.ENTER)

# Attendre les résultats
wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test-id='project-card']"))
)

# Récupérer les projets
projets = driver.find_elements(By.CSS_SELECTOR, "div[data-test-id='project-card']")

# Afficher les 5 premiers résultats
for projet in projets[:5]:
    try:
        titre = projet.find_element(By.TAG_NAME, "h3").text
        print(titre)
    except:
        print("Titre non trouvé")

time.sleep(5)
driver.quit()
