from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class TestAdecco:

    def setup(self):
        """Initialisation du navigateur"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def test_homepage_load(self):
        """Test 1 : Vérifier que la page d'accueil charge correctement"""
        self.driver.get("https://www.adecco.fr")

        try:
            self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("Page d'accueil chargée avec succès")
        except TimeoutException:
            print("Erreur : la page d'accueil ne s'est pas chargée")

    def test_job_search(self):
        """Test 2 : Effectuer une recherche d'emploi"""
        self.driver.get("https://www.adecco.fr")

        try:
            # Accepter les cookies si présents
            try:
                cookie_button = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
                )
                cookie_button.click()
                print("Cookies acceptés")
            except:
                pass

            # Localiser le champ de recherche
            search_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "k"))
            )

            search_input.clear()
            search_input.send_keys("informatique")
            search_input.send_keys(Keys.RETURN)

            print("Recherche lancée")

            # Attendre les résultats
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "job-offer"))
            )

            print("Résultats affichés")

        except TimeoutException:
            print("Erreur : les résultats ne sont pas apparus")

    def teardown(self):
        """Fermeture du navigateur"""
        time.sleep(3)
        self.driver.quit()
        print("Navigateur fermé")


if __name__ == "__main__":
    test = TestAdecco()
    test.setup()

    try:
        test.test_homepage_load()
        test.test_job_search()
    finally:
        test.teardown()