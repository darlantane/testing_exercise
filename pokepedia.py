from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class TestPokepedia:

    def setup(self):
        """Initialisation du navigateur"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def accept_cookies(self):
        """Accepter les cookies si présent"""
        try:
            cookie_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_button.click()
            print("Cookies acceptés")
        except:
            pass

    def test_homepage_load(self):
        """Test 1 : Vérifier que la page d'accueil charge"""
        self.driver.get("https://www.pokepedia.fr/")
        try:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            print("Page d'accueil chargée avec succès")
        except TimeoutException:
            print("Erreur : la page d'accueil ne s'est pas chargée")

    def test_logo_presence(self):
        """Test 2 : Vérifier que le logo est présent"""
        self.driver.get("https://www.pokepedia.fr/")
        self.accept_cookies()

        try:
            logo = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "mw-wiki-logo"))
            )
            print("Logo trouvé :", logo.is_displayed())
        except TimeoutException:
            print("Logo non trouvé")

    def test_pokemon_search(self):
        """Test 3 : Recherche Pokémon"""
        self.driver.get("https://www.pokepedia.fr/")
        self.accept_cookies()

        try:
            search_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "searchInput"))
            )

            search_input.clear()
            search_input.send_keys("Pikachu")
            search_input.send_keys(Keys.RETURN)

            self.wait.until(
                EC.presence_of_element_located((By.ID, "firstHeading"))
            )

            print("Recherche Pokémon réussie")

        except TimeoutException:
            print("Erreur lors de la recherche Pokémon")

    def test_invalid_search(self):
        """Test 4 : Recherche invalide"""
        self.driver.get("https://www.pokepedia.fr/")
        self.accept_cookies()

        try:
            search_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "searchInput"))
            )

            search_input.send_keys("PokemonQuiExistePas123")
            search_input.send_keys(Keys.RETURN)

            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "searchresults"))
            )

            print("Résultats de recherche affichés pour une recherche invalide")

        except TimeoutException:
            print("La recherche invalide n'a pas fonctionné")

    def test_navigation_to_pokemon(self):
        """Test 5 : Cliquer sur un lien Pokémon"""
        self.driver.get("https://www.pokepedia.fr/Pikachu")

        try:
            heading = self.wait.until(
                EC.presence_of_element_located((By.ID, "firstHeading"))
            )

            if "Pikachu" in heading.text:
                print("Navigation vers la page Pikachu réussie")

        except TimeoutException:
            print("Impossible d'accéder à la page Pikachu")

    def test_pokemon_image(self):
        """Test 6 : Vérifier qu'une image Pokémon est affichée"""
        self.driver.get("https://www.pokepedia.fr/Pikachu")

        try:
            image = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.infobox img"))
            )

            print("Image Pokémon chargée :", image.is_displayed())

        except TimeoutException:
            print("Image Pokémon non trouvée")

    def teardown(self):
        """Fermeture du navigateur"""
        time.sleep(3)
        self.driver.quit()
        print("Navigateur fermé")


if __name__ == "__main__":
    test = TestPokepedia()
    test.setup()

    try:
        test.test_homepage_load()
        test.test_logo_presence()
        test.test_pokemon_search()
        test.test_invalid_search()
        test.test_navigation_to_pokemon()
        test.test_pokemon_image()
    finally:
        test.teardown()