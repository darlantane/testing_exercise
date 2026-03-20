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
            assert titre.strip() != "", f"Offre {i} sans titre"
            print(f"Offre {i+1} : {titre}")
        except NoSuchElementException:
            print(f"Offre {i+1} : élément h3 introuvable")

    # Test 5 : vérifier la présence d’un bouton
    try:
        bouton = driver.find_element(By.CSS_SELECTOR, "button")
        assert bouton.is_displayed(), "Bouton non visible"
        print("Bouton trouvé et visible")
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

    # Test 7 : cliquer sur une offre et vérifier navigation
    try:
        premier_lien = annonces[0].find_element(By.TAG_NAME, "a")
        url_avant = driver.current_url
        premier_lien.click()

        wait.until(EC.url_changes(url_avant))
        assert driver.current_url != url_avant, "Navigation échouée"

        print("Navigation vers une offre OK")

        driver.back()
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article")))

    except Exception as e:
        print(f"Test navigation échoué : {e}")

    # Test 8 : vérifier présence pagination ou scroll
    try:
        pagination = driver.find_elements(By.CSS_SELECTOR, "a[rel='next']")
        if pagination:
            print("Pagination détectée")
        else:
            print("Pas de pagination détectée (scroll infini probable)")
    except:
        print("⚠️ Erreur test pagination")

    # Test 9 : vérifier qu'aucune offre n'est dupliquée
    titres = []
    for offre in annonces[:10]:
        try:
            titre = offre.find_element(By.TAG_NAME, "h3").text
            titres.append(titre)
        except:
            pass

    assert len(titres) == len(set(titres)), "Doublons détectés"
    print("Pas de doublons dans les offres")

    # Test 10 : vérifier que les offres ont une localisation ou info
    for i, offre in enumerate(annonces[:5]):
        texte = offre.text
        assert len(texte.strip()) > 20, f"Offre {i} trop vide"
    print("Contenu des offres OK")

    # Test 11 : test du temps de chargement (basique)
    start = time.time()
    driver.refresh()
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article")))
    load_time = time.time() - start

    assert load_time < 10, f"Temps de chargement trop long : {load_time}s"
    print(f"Temps de chargement : {load_time:.2f}s")

    # Test 12 : vérifier que les images (si présentes) ont une source
    images = driver.find_elements(By.TAG_NAME, "img")
    for img in images[:5]:
        src = img.get_attribute("src")
        assert src is not None and src != "", "Image sans source"
    print("Images OK")

except TimeoutException:
    print("Timeout : les annonces ne se chargent pas")

except AssertionError as e:
    print(e)

finally:
    time.sleep(5)
    driver.quit()