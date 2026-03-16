from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://recrutement.ldc.fr/fr/annonces")
driver.maximize_window()

wait = WebDriverWait(driver, 15)

# Attendre que les annonces soient chargées
annonces = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article"))
)

# Récupérer toutes les annonces
offres = driver.find_elements(By.CSS_SELECTOR, "article")

print("Nombre d'offres trouvées :", len(offres))

# Afficher les 5 premières offres
for offre in offres[:5]:
    try:
        titre = offre.find_element(By.TAG_NAME, "h3").text
        print(titre)
    except:
        print("Titre non trouvé")

time.sleep(5)
driver.quit()