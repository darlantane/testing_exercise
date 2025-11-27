import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.wikipedia.org/"
keyword = "Dune"


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    return webdriver.Chrome(options=chrome_options)


def test_wikipedia_search():
    driver = get_driver()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(url)

        # Accepter les cookies
        try:
            cookie_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button#accept-optional-cookies"))
            )
            cookie_btn.click()
        except:
            pass

        # Recherche
        search_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input#searchInput"))
        )
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.ENTER)

        # Vérifier que le titre de l’article est présent
        article_title = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#firstHeading"))
        )
        assert article_title.text != ""

    finally:
        driver.quit()
