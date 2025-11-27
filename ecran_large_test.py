import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.ecranlarge.com/"
keyword = "Dune"


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")  # ← empêche la popup navigateur
    return webdriver.Chrome(options=chrome_options)


def test():
    driver = get_driver()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(url)

        # Accepter cookies
        try:
            accept_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#didomi-notice-agree-button"))
            )
            accept_button.click()
        except:
            pass

        # Recherche
        search_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Bouton de recherche']"))
        )
        search_button.click()

        search_input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='search']"))
        )
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.ENTER)

        results = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article"))
        )
        assert len(results) > 0

        first = results[0].find_element(By.TAG_NAME, "a")
        first.click()

        article_title = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h1"))
        )
        assert article_title.text != ""

    finally:
        driver.quit()
