from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService # Similar thing for firefox also!
from subprocess import CREATE_NO_WINDOW 
import time
import sys

chrome_options = Options()
chrome_options.headless = True
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

chrome_service = ChromeService('chromedriver')
chrome_service.creationflags = CREATE_NO_WINDOW

driver = webdriver.Chrome(r"chromedriver", options=chrome_options, service=chrome_service)

USERNAME = ""
PASSWORD = ""

def main():
    while True:
        if site_login():
            print("Retry in 3 hours.")
            time.sleep(10800)
        else:
            print("Retry in 10 seconds.")
            time.sleep(10)

def site_login():
    driver.get("https://portal-front.wifirst.net/")
    delay = 1.5
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'email')))
    except TimeoutException:
        print("Could not retrieve the page elements.")
        return False
    driver.find_element(By.NAME, 'email').send_keys(USERNAME)
    driver.find_element(By.NAME, 'password').send_keys(PASSWORD)
    # Submit the form
    driver.find_element(By.XPATH, '//button[@type="submit"][text()="Connexion"]').click()
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//button[@type="button"][text()="Se déconnecter"]')))
    except TimeoutException:
        print("Could not retrieve the logged-in page elements.")
        # Make a screenshot
        driver.save_screenshot("screenshot.png")
        return False

    print("Login successful.")
    return True

main()