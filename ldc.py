from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

driver = webdriver.Chrome()
driver.get("https://recrutement.ldc.fr/fr/annonces")
driver.maximize_window()

wait = WebDriverWait(driver, 15)

try:
    # Test 1 : vérifier que la page est bien chargée
    assert "LDC" in driver.title
    print("Page chargée correctement")

    # Test 2 : attendre les annonces
    annonces = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article"))
    )

    # Test 3 : vérifier qu'il y a des offres
    assert len(annonces) > 0, "Aucune offre trouvée"
    print(f"{len(annonces)} offres trouvées")

    # Test 4 : vérifier que chaque offre contient un titre
    for i, offre in enumerate(annonces[:5]):
        try:
            titre = offre.find_element(By.TAG_NAME, "h3").text
            
            # Vérifie que le titre n'est pas vide
            assert titre.strip() != "", f"Offre {i} sans titre"

            print(f"Offre {i+1} : {titre}")

        except NoSuchElementException:
            print(f"Offre {i+1} : élément h3 introuvable")

    # Test 5 : vérifier la présence d’un bouton ou filtre (exemple)
    try:
        bouton = driver.find_element(By.CSS_SELECTOR, "button")
        print("Bouton trouvé sur la page")
    except NoSuchElementException:
        print("Aucun bouton trouvé")

    # Test 6 : vérifier que les URLs sont valides
    for i, offre in enumerate(annonces[:5]):
        try:
            lien = offre.find_element(By.TAG_NAME, "a").get_attribute("href")
            assert lien.startswith("http"), f"Lien invalide pour offre {i}"
            print(f"Lien OK : {lien}")
        except:
            print(f"Pas de lien pour offre {i+1}")

except TimeoutException:
    print("Timeout : les annonces ne se chargent pas")

except AssertionError as e:
    print(e)

finally:
    time.sleep(5)
    driver.quit()