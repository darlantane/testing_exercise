from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class TestIndeed:

    def setup(self):
        """Initialisation du navigateur"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def accept_cookies(self):
        """Méthode utilitaire pour accepter les cookies"""
        try:
            cookie_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_button.click()
            print("Cookies acceptés")
        except:
            pass

    def test_homepage_load(self):
        """Test 1 : Vérifier que la page d'accueil charge correctement"""
        self.driver.get("https://fr.indeed.com")

        try:
            self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("Page d'accueil Indeed chargée avec succès")
        except TimeoutException:
            print("Erreur : la page d'accueil ne s'est pas chargée")

    def test_page_title(self):
        """Test 2 : Vérifier que le titre contient 'Indeed'"""
        self.driver.get("https://fr.indeed.com")
        if "Indeed" in self.driver.title:
            print("Titre de page correct")
        else:
            print("Erreur : titre incorrect")

    def test_search_fields_presence(self):
        """Test 3 : Vérifier la présence des champs de recherche"""
        self.driver.get("https://fr.indeed.com")
        self.accept_cookies()

        try:
            self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
            self.wait.until(EC.presence_of_element_located((By.NAME, "l")))
            print("Champs de recherche présents")
        except TimeoutException:
            print("Erreur : champs de recherche non trouvés")

    def test_job_search(self):
        """Test 4 : Effectuer une recherche d'emploi"""
        self.driver.get("https://fr.indeed.com")
        self.accept_cookies()

        try:
            search_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_input.clear()
            search_input.send_keys("informatique")

            location_input = self.driver.find_element(By.NAME, "l")
            location_input.clear()
            location_input.send_keys("Paris")
            location_input.send_keys(Keys.RETURN)

            print("Recherche lancée")

            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.job_seen_beacon"))
            )
            print("Résultats affichés")

        except TimeoutException:
            print("Erreur : les résultats ne sont pas apparus")

    def test_first_result_contains_title(self):
        """Test 5 : Vérifier qu’un résultat contient un titre"""
        self.test_job_search()

        try:
            job_title = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h2.jobTitle"))
            )
            print(f"Titre trouvé : {job_title.text}")
        except TimeoutException:
            print("Erreur : aucun titre trouvé")

    def test_click_first_job(self):
        """Test 6 : Cliquer sur la première offre"""
        self.test_job_search()

        try:
            first_job = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "h2.jobTitle a"))
            )
            first_job.click()
            print("Première offre cliquée")
        except TimeoutException:
            print("Erreur : impossible de cliquer sur l'offre")

    def test_pagination(self):
        """Test 7 : Vérifier la pagination"""
        self.test_job_search()

        try:
            next_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Suivant']"))
            )
            next_button.click()
            print("Pagination fonctionnelle")
        except TimeoutException:
            print("Erreur : bouton pagination non trouvé")

    def test_navigation_companies_page(self):
        """Test 8 : Vérifier navigation vers la page Entreprises"""
        self.driver.get("https://fr.indeed.com")
        self.accept_cookies()

        try:
            companies_link = self.wait.until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Entreprises"))
            )
            companies_link.click()

            self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            print("Navigation vers page Entreprises réussie")
        except TimeoutException:
            print("Erreur : navigation vers page Entreprises échouée")

    def teardown(self):
        """Fermeture du navigateur"""
        time.sleep(3)
        self.driver.quit()
        print("Navigateur fermé")


if __name__ == "__main__":
    test = TestIndeed()
    test.setup()

    try:
        test.test_homepage_load()
        test.test_page_title()
        test.test_search_fields_presence()
        test.test_job_search()
        test.test_first_result_contains_title()
        test.test_click_first_job()
        test.test_pagination()

    finally:
        test.teardown()