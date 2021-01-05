import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def create_driver(system, url, use_profile, start_maximized):
    if system == 'Darwin':
        path = 'chrome_mac/chromedriver'
    elif system == 'Linux':
        path = 'chrome_linux/chromedriver'
    elif system == 'Windows':
        path = os.getcwd() + '\chrome_windows\chromedriver.exe'
    else:
        raise OSError(f'Operating system {system} is not supported')

    chrome_options = Options()
    chrome_options.add_argument("--app=" + url)
    if start_maximized:
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--kiosk")
    if use_profile:
        chrome_options.add_argument("user-data-dir=chrome-user-data-dir")
    
    driver = webdriver.Chrome(
        executable_path=path,
        chrome_options=chrome_options
    )
    return driver

def wait_for_shield_invisibility(driver, duration=0.25):
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, 'ut-click-shield showing interaction'))
    )
    sleep(duration)
