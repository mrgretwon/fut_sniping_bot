from time import sleep

import atexit
import random

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.config import URL, INCREASE_COUNT
from src.email_manager import get_access_code
from src.helpers import wait_for_shield_invisibility, create_driver

class Bot:
    def __init__(self):
        self.driver = create_driver()
        self.action = ActionChains(self.driver)
        self.driver.get(URL)

        atexit.register(self.cleanup)
        print("Starting sniping bot...")

    def cleanup(self):
        print("Running cleanup...")
        self.quit()

    def quit(self):
        self.driver.quit()

    def go_to_login_page(self):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@class="ut-login-content"]//button'))
        )
        print("Logging in...")
        sleep(2)
        self.driver.find_element(By.XPATH, '//*[@class="ut-login-content"]//button').click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'email'))
        )

    def login(self, user):
        self.go_to_login_page()

        self.driver.find_element(By.ID, 'email').send_keys(user["email"])
        self.driver.find_element(By.ID, 'password').send_keys(user["password"])
        self.driver.find_element(By.ID, 'btnLogin').click()

        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.ID, 'btnSendCode'))
        ).click()

        access_code = get_access_code()
        self.driver.find_element(By.ID, 'oneTimeCode').send_keys(access_code)
        self.driver.find_element(By.ID, 'btnSubmit').click()

        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'icon-transfer'))
        )
        sleep(2)

    def login_manually(self):
        self.go_to_login_page()

        print("Enter your account credentials and click login button.")
        print("Waiting 5 minutes...")

        WebDriverWait(self.driver, 300).until(
            EC.element_to_be_clickable((By.ID, 'btnSendCode'))
        ).click()

        print("Provide EA access code and click submit button.")
        print("Waiting 5 minutes...")

        WebDriverWait(self.driver, 300).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'icon-transfer'))
        )
        sleep(2)

    def wait_for_login(self):
        print("Waiting 5 minutes for Login...")
        WebDriverWait(self.driver, 300).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'icon-transfer'))
        )
        sleep(2)

    def go_to_transfer_market(self):
        self.driver.find_element(By.CLASS_NAME, 'icon-transfer').click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'ut-tile-transfer-market'))
        )
        sleep(1)
        self.driver.find_element(By.CLASS_NAME, 'ut-tile-transfer-market').click()

    def get_coins(self):
        return int(
            self.driver.find_element(By.CLASS_NAME, 'view-navbar-currency-coins').text
                .replace(" ", "")
                .replace(".", "")
                .replace(",", "")
            )

    def search_player(self, player, max_price, max_player_count):
        count = 1
        success_count = 0
        coins = self.get_coins()
        print("Number of coins: " + str(coins))

        while coins >= max_price and success_count < max_player_count:
            if count % INCREASE_COUNT == 0:
                min_price_input = self.driver.find_element(By.XPATH, '(//input[contains(@class, "numericInput")])[3]')
                min_price_input.click()
                min_price_input.send_keys(0)

            self.driver.find_element(By.XPATH, '(//*[@class="button-container"]/button)[2]').click()
            result = WebDriverWait(self.driver, 10).until(lambda d: d.find_elements(By.CLASS_NAME, 'no-results-icon') or
                                                                    d.find_elements(By.CLASS_NAME, 'DetailView'))[0]

            # Buy a player when result appears
            if "DetailView" in result.get_attribute("class"):
                coins = self.get_coins()

                try:
                    self.driver.find_element(By.XPATH, '//button[contains(@class, "buyButton")]').click()
                except WebDriverException:
                    wait_for_shield_invisibility(self.driver, 0.1)
                    self.driver.find_element(By.XPATH, '//button[contains(@class, "buyButton")]').click()

                self.driver.find_element(By.XPATH, '//div[contains(@class,"view-modal-container")]//button').click()
                sleep(random.randint(1, 9))

                new_coins = self.get_coins()
                if coins == new_coins:
                    print("Found something, but it was too late.")
                else:
                    price = coins - new_coins
                    print("Success! You bought " + player + " for " + str(price) + " coins.")
                    coins = new_coins
                    success_count += 1

            try:
                self.driver.find_element(By.XPATH, '//button[contains(@class, "ut-navigation-button-control")]').click()
            except WebDriverException:
                wait_for_shield_invisibility(self.driver, 0.1)
                self.driver.find_element(By.XPATH, '//button[contains(@class, "ut-navigation-button-control")]').click()

            inc_max_price_button = self.driver.find_element(By.XPATH, '(//div[@class="price-filter"]//button)[6]')

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '(//div[@class="price-filter"]//button)[6]'))
            )

            wait_for_shield_invisibility(self.driver)

            inc_max_price_button.click()
            count += 1
            sleep(random.randint(1, 9)/10)

        if success_count == max_player_count:
            print("You bought " + str(max_player_count) + " players. Assign them and rerun the bot.")
        else:
            print("You have not enought coins for more players.")

    def buy_players(self, player, max_price, max_player_count):
        try:
            self.go_to_transfer_market()

            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'ut-player-search-control'))
            )
            wait_for_shield_invisibility(self.driver)

            self.driver.find_element(By.XPATH, '//div[contains(@class, "ut-player-search-control")]//input').click()
            sleep(0.1)
            self.driver.find_element(By.XPATH, '//div[contains(@class, "ut-player-search-control")]//input').send_keys(player)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//ul[contains(@class, "playerResultsList")]/button'))
            )
            sleep(1)

            self.driver.find_element(By.XPATH, '//ul[contains(@class, "playerResultsList")]/button').click()

            self.driver.find_element(By.XPATH, '(//input[@class="numericInput"])[4]').click()
            sleep(0.1)
            self.driver.find_element(By.XPATH, '(//input[@class="numericInput"])[4]').send_keys(max_price)

            print("Looking for " + player + " with max price " + str(max_price) + "...")
            self.search_player(player, max_price, max_player_count)

        except TimeoutException:
            print("Error, check the browser")
