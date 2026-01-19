from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://www.ulule.com")
driver.maximize_window()
  
    
bouton_recherche = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.ID, "icon-search"))
    )
bouton_recherche.click()


barre_recherche = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH,"//*[@id='search']"))
)
barre_recherche.send_keys("justloui")
barre_recherche.send_keys(Keys.ENTER)


WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#react-app-root > div.yteSSds > div > div > div > ul"))
)


projets = driver.find_elements(By.CSS_SELECTOR, "#react-app-root > div.yteSSds > div > div > div > ul")

for projet in projets[:5]:
    print(projet.text)
    

time.sleep(5)
driver.quit()