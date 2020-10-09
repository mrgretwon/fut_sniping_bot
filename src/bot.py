import os
from time import sleep

from gtts import gTTS
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.config import create_driver, ALLOW_NOTIFICATIONS
from src.config import URL


class Bot:
    def __init__(self):
        self.driver = create_driver()
        self.driver.get(URL)
        print("Starting sniping bot...")

    @staticmethod
    def read(text, language='pl'):
        if ALLOW_NOTIFICATIONS:
            message = gTTS(text=text, lang=language, slow=False)
            message.save("message.mp3")
            os.system("mpg123 message.mp3")
            os.system("rm message.mp3")

    def login(self, user):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@class="ut-login-content"]//button'))
        )
        sleep(2)
        self.driver.find_element(By.XPATH, '//*[@class="ut-login-content"]//button').click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'email'))
        )

        print("Logging in...")
        self.driver.find_element(By.ID, 'email').send_keys(user["email"])
        self.driver.find_element(By.ID, 'password').send_keys(user["password"])
        self.driver.find_element(By.ID, 'btnLogin').click()

        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, 'btnSendCode'))
        ).click()

        print("You have 5 minutes for providing access code.\nWaiting...")

        WebDriverWait(self.driver, 300).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'icon-transfer'))
        )
        sleep(2)

    def go_to_transfer_market(self):
        self.driver.find_element(By.CLASS_NAME, 'icon-transfer').click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'ut-tile-transfer-market'))
        )
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'ut-click-shield showing interaction'))
        )
        sleep(1)
        self.driver.find_element(By.CLASS_NAME, 'ut-tile-transfer-market').click()

    def search_player(self, inc=True):
        dec_button = self.driver.find_element(By.XPATH, '(//div[@class="price-filter"]//button)[7]')
        inc_button = self.driver.find_element(By.XPATH, '(//div[@class="price-filter"]//button)[8]')

        if inc:
            inc_button.click()
        else:
            dec_button.click()

        self.driver.find_element(By.XPATH, '(//*[@class="button-container"]/button)[2]').click()

        result = WebDriverWait(self.driver, 10).until(lambda d: d.find_elements(By.CLASS_NAME, 'no-results-icon') or
                                                       d.find_elements(By.CLASS_NAME, 'DetailView'))[0]

        if "DetailView" in result.get_attribute("class"):
            self.driver.find_element(By.XPATH, '//button[contains(@class, "buyButton")]').click()
            self.driver.find_element(By.XPATH, '//div[contains(@class,"view-modal-container")]//button').click()

            print("Success!")
            self.read("Tutututurututu!")
        else:
            self.driver.find_element(By.XPATH, '//button[contains(@class, "ut-navigation-button-control")]').click()
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '(//*[@class="button-container"]/button)[2]'))
            )
            sleep(0.25)

            self.search_player(not inc)

    def buy_player(self, player, price):
        self.go_to_transfer_market()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'ut-player-search-control'))
        )
        sleep(2)

        self.driver.find_element(By.XPATH, '//div[contains(@class, "ut-player-search-control")]//input').click()
        sleep(1)
        self.driver.find_element(By.XPATH, '//div[contains(@class, "ut-player-search-control")]//input').send_keys(player)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//ul[contains(@class, "playerResultsList")]/button'))
        )
        sleep(1)

        self.driver.find_element(By.XPATH, '//ul[contains(@class, "playerResultsList")]/button').click()

        self.driver.find_element(By.XPATH, '(//input[@class="numericInput"])[4]').click()
        sleep(0.5)
        self.driver.find_element(By.XPATH, '(//input[@class="numericInput"])[4]').send_keys(price)

        print("Looking for " + player + " with max price " + str(price) + "...")

        self.search_player()
