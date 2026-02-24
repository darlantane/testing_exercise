from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class TestBDFugue:

    def setup(self):
        """Initialisation du navigateur"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def accept_cookies(self):
        """Accepter les cookies si la popup apparaît"""
        try:
            cookie_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
            )
            cookie_button.click()
            print("Cookies acceptés")
        except:
            pass

    def test_homepage_load(self):
        """Test 1 : Vérifier que la page d'accueil charge"""
        self.driver.get("https://www.bdfugue.com")

        try:
            self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("Page d'accueil BDFugue chargée avec succès")
        except TimeoutException:
            print("Erreur : la page d'accueil ne s'est pas chargée")

    def test_page_title(self):
        """Test 2 : Vérifier que le titre contient 'BD' ou 'BDFugue'"""
        self.driver.get("https://www.bdfugue.com")

        if "BD" in self.driver.title or "BDFugue" in self.driver.title:
            print("Titre de page correct")
        else:
            print("Erreur : titre incorrect")

    def test_search_field_presence(self):
        """Test 3 : Vérifier la présence du champ de recherche"""
        self.driver.get("https://www.bdfugue.com")
        self.accept_cookies()

        try:
            self.wait.until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            print("Champ de recherche présent")
        except TimeoutException:
            print("Erreur : champ de recherche non trouvé")

    def test_product_search(self):
        """Test 4 : Effectuer une recherche de BD"""
        self.driver.get("https://www.bdfugue.com")
        self.accept_cookies()

        try:
            search_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_input.clear()
            search_input.send_keys("Kidz")
            search_input.send_keys(Keys.RETURN)

            print("Recherche lancée")

            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-item"))
            )
            print("Résultats affichés")

        except TimeoutException:
            print("Erreur : les résultats ne sont pas apparus")

    def test_first_result_contains_title(self):
        """Test 5 : Vérifier qu’un résultat contient un titre"""
        self.test_product_search()

        try:
            product_title = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-item a.product-item-link"))
            )
            print(f"Titre trouvé : {product_title.text}")
        except TimeoutException:
            print("Erreur : aucun titre trouvé")

    def test_click_first_product(self):
        """Test 6 : Cliquer sur le premier produit"""
        self.test_product_search()

        try:
            first_product = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".product-item a.product-item-link"))
            )
            first_product.click()
            print("Premier produit cliqué")

            self.wait.until(
                EC.presence_of_element_located((By.ID, "product-addtocart-button"))
            )
            print("Page produit affichée")

        except TimeoutException:
            print("Erreur : impossible de cliquer sur le produit")

    def test_navigation_promotions(self):
        """Test 7 : Vérifier navigation vers la page Promotions"""
        self.driver.get("https://www.bdfugue.com")
        self.accept_cookies()

        try:
            promo_link = self.wait.until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Promotions"))
            )
            promo_link.click()

            self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            print("Navigation vers page Promotions réussie")
        except TimeoutException:
            print("Erreur : navigation vers page Promotions échouée")

    def teardown(self):
        """Fermeture du navigateur"""
        time.sleep(3)
        self.driver.quit()
        print("Navigateur fermé")


if __name__ == "__main__":
    test = TestBDFugue()
    test.setup()

    try:
        test.test_homepage_load()
        test.test_page_title()
        test.test_search_field_presence()
        test.test_product_search()
        test.test_first_result_contains_title()
        test.test_click_first_product()
        test.test_navigation_promotions()

    finally:
        test.teardown()