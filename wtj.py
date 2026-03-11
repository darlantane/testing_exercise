from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


class TestWelcomeToTheJungle:

    def setup(self):
        """Initialisation du navigateur"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def accept_cookies(self):
        """Accepter les cookies si présents"""
        try:
            cookie_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "axeptio_btn_acceptAll"))
            )
            cookie_button.click()
            print("Cookies acceptés")
        except TimeoutException:
            pass

    def test_homepage_load(self):
        """Test 1 : Vérifier que la page d'accueil charge"""
        self.driver.get("https://www.welcometothejungle.com/fr")
        try:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print("Page d'accueil chargée avec succès")
        except TimeoutException:
            print("Erreur : la page d'accueil ne s'est pas chargée")

    def test_logo_presence(self):
        """Test 2 : Vérifier la présence du logo"""
        self.driver.get("https://www.welcometothejungle.com/fr")
        self.accept_cookies()
        try:
            logo = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "header img"))
            )
            print("Logo trouvé :", logo.is_displayed())
        except TimeoutException:
            print("Logo non trouvé")

    def test_job_search(self):
        """Test 3 : Recherche d'emploi"""
        self.driver.get("https://www.welcometothejungle.com/fr")
        self.accept_cookies()
        try:
            search_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "query"))
            )
            search_input.clear()
            search_input.send_keys("Développeur")
            search_input.send_keys(Keys.RETURN)
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "main")))
            print("Recherche d'emploi réussie")
        except TimeoutException:
            print("Erreur lors de la recherche d'emploi")

    def test_invalid_search(self):
        """Test 4 : Recherche invalide"""
        self.driver.get("https://www.welcometothejungle.com/fr")
        self.accept_cookies()
        try:
            search_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "query"))
            )
            search_input.send_keys("xxxxxxxxxxxxxxxxxxxx")
            search_input.send_keys(Keys.RETURN)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
            print("Recherche invalide effectuée")
        except TimeoutException:
            print("La recherche invalide n'a pas fonctionné")

    def test_navigation_to_company(self):
        """Test 5 : Navigation vers une entreprise"""
        self.driver.get("https://www.welcometothejungle.com/fr/companies")
        try:
            company = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='companies/']"))
            )
            company.click()
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            print("Navigation vers une page entreprise réussie")
        except TimeoutException:
            print("Impossible d'accéder à la page entreprise")

    def test_company_image(self):
        """Test 6 : Vérifier qu'une image entreprise est affichée"""
        self.driver.get("https://www.welcometothejungle.com/fr/companies")
        try:
            image = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img"))
            )
            print("Image entreprise chargée :", image.is_displayed())
        except TimeoutException:
            print("Image entreprise non trouvée")

    def test_header_links(self):
        """Test 7 : Vérification des liens principaux du header"""
        self.driver.get("https://www.welcometothejungle.com/fr")
        self.accept_cookies()
        try:
            header_links = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "header a"))
            )
            for link in header_links:
                print("Lien header :", link.get_attribute("href"))
            print("Tous les liens du header trouvés")
        except TimeoutException:
            print("Impossible de trouver les liens du header")

    def test_footer_presence(self):
        """Test 8 : Vérification du footer"""
        self.driver.get("https://www.welcometothejungle.com/fr")
        try:
            footer = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "footer"))
            )
            print("Footer trouvé :", footer.is_displayed())
        except TimeoutException:
            print("Footer non trouvé")

    def test_job_filters(self):
        """Test 9 : Vérification des filtres de recherche d'emploi"""
        self.driver.get("https://www.welcometothejungle.com/fr/jobs")
        self.accept_cookies()
        try:
            location_filter = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='filter-location']"))
            )
            category_filter = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='filter-category']"))
            )
            print("Filtres trouvés :", location_filter.is_displayed(), category_filter.is_displayed())
        except TimeoutException:
            print("Filtres non trouvés")

    def teardown(self):
        """Fermeture du navigateur"""
        time.sleep(2)
        self.driver.quit()
        print("Navigateur fermé")


if __name__ == "__main__":
    test = TestWelcomeToTheJungle()
    test.setup()
    try:
        test.test_homepage_load()
        test.test_logo_presence()
        test.test_job_search()
        test.test_invalid_search()
        test.test_navigation_to_company()
        test.test_company_image()
        test.test_header_links()
        test.test_footer_presence()
        test.test_job_filters()
    finally:
        test.teardown()