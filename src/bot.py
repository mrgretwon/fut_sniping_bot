from time import sleep
import platform
import atexit
import random
import enum

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.config import URL, USE_CHROME_PROFILE, START_MAXIMIZED, INCREASE_COUNT
from src.email_manager import get_access_code
from src.helpers import wait_for_shield_invisibility, create_driver

class Bot:
    def __init__(self):
        self.system = platform.system()
        self.driver = create_driver(self.system, URL, USE_CHROME_PROFILE, START_MAXIMIZED)
        self.action = ActionChains(self.driver)

        atexit.register(self.cleanup)
        print("Starting sniping bot...")

    def cleanup(self):
        print("Running cleanup...")
        self.quit()

    def quit(self):
        #self.driver.quit()
        pass

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
        print("Waiting max. 5 minutes...")

        WebDriverWait(self.driver, 300).until(
            EC.element_to_be_clickable((By.ID, 'btnSendCode'))
        ).click()

        print("Provide EA access code and click submit button.")
        print("Waiting max. 5 minutes...")

        WebDriverWait(self.driver, 300).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'icon-transfer'))
        )
        sleep(2)

    def wait_for_login(self):
        print("Waiting max. 5 minutes for Login...")
        WebDriverWait(self.driver, 300).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'icon-transfer'))
        )
        sleep(2)

    def get_coins(self):
        return int(
            self.driver.find_element(By.CLASS_NAME, 'view-navbar-currency-coins').text
                .replace(" ", "")
                .replace(".", "")
                .replace(",", "")
            )

    def go_to_transfer_market_search(self):
        self.driver.find_element(By.CLASS_NAME, 'icon-transfer').click()

        # wait until loaded - transfer market
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'ut-tile-transfer-market'))
        )
        sleep(random.randint(3, 9)/10)
        self.driver.find_element(By.CLASS_NAME, 'ut-tile-transfer-market').click()

        # wait until loaded - transfer market search
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'ut-player-search-control'))
        )
        wait_for_shield_invisibility(self.driver)
        sleep(random.randint(3, 9)/10)

    def fill_transfer_search(self, player, max_price):
        # set player name
        self.driver.find_element(By.XPATH, '//div[contains(@class, "ut-player-search-control")]//input').click()
        sleep(random.randint(3, 9)/10)
        self.driver.find_element(By.XPATH, '//div[contains(@class, "ut-player-search-control")]//input').send_keys(player)

        # select player in dropdown
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//ul[contains(@class, "playerResultsList")]/button'))
        )
        sleep(random.randint(3, 9)/10)
        self.driver.find_element(By.XPATH, '//ul[contains(@class, "playerResultsList")]/button').click()

        # set max buy price
        self.driver.find_element(By.XPATH, '(//input[@class="numericInput"])[4]').click()
        sleep(random.randint(3, 9)/10)
        self.driver.find_element(By.XPATH, '(//input[@class="numericInput"])[4]').send_keys(max_price)
        sleep(random.randint(3, 9)/10)

    def begin_transfer_market_search(self):
        sleep(random.randint(3, 9)/10)
        self.driver.find_element(By.XPATH, '(//*[@class="button-container"]/button)[2]').click()
        #WebDriverWait(self.driver, 10).until(lambda d: d.find_elements(By.CLASS_NAME, 'no-results-icon') or
        #                                               d.find_elements(By.CLASS_NAME, 'DetailView'))[0]

    def end_transfer_market_search(self):
        sleep(random.randint(3, 9)/10)
        try:
            self.driver.find_element(By.XPATH, '//button[contains(@class, "ut-navigation-button-control")]').click()
        except WebDriverException:
            wait_for_shield_invisibility(self.driver, 0.1)
            self.driver.find_element(By.XPATH, '//button[contains(@class, "ut-navigation-button-control")]').click()

    def increase_instant_buy_min_price(self):
        sleep(random.randint(3, 9)/10)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '(//div[@class="price-filter"]//button)[6]'))
        )
        wait_for_shield_invisibility(self.driver)
        sleep(random.randint(3, 9)/10)
        self.driver.find_element(By.XPATH, '(//div[@class="price-filter"]//button)[6]').click()

    def reset_instant_buy_min_price(self, count):
        sleep(random.randint(3, 9)/10)
        min_price_input = self.driver.find_element(By.XPATH, '(//input[contains(@class, "numericInput")])[3]')
        min_price_input.click()
        for x in range(4):
            min_price_input.send_keys("\u0008")
        self.driver.find_element(By.XPATH, '(//div[@class="price-filter"]//button)[6]').click()

    def buy_player(self, player):
        coins = self.get_coins()

        try:
            self.driver.find_element(By.XPATH, '//button[contains(@class, "buyButton")]').click()
        except WebDriverException:
            wait_for_shield_invisibility(self.driver, 0.1)
            self.driver.find_element(By.XPATH, '//button[contains(@class, "buyButton")]').click()

        self.driver.find_element(By.XPATH, '//div[contains(@class,"view-modal-container")]//button').click()
        sleep(random.randint(1, 5))

        new_coins = self.get_coins()
        if coins == new_coins:
            print("Found something, but it was too late.")
            return 0
        else:
            price = coins - new_coins
            print("Success! You bought " + player + " for " + str(price) + " coins. Remaining coins: " + str(new_coins))
            return price

    def try_buy_player(self, player, expected_player_rating):
        element = WebDriverWait(self.driver, 10).until(lambda d: d.find_elements(By.CLASS_NAME, 'no-results-icon') or
                                                                 d.find_elements(By.CLASS_NAME, 'DetailView'))[0]
        if "DetailView" in element.get_attribute("class"):
            if expected_player_rating is None:
                return self.buy_player(player)
            else:
                player_rating = int(self.driver.find_element(By.XPATH, "//div[contains(@class, 'tns-slide-active')]//div[@class='rating']").text)
                if player_rating == expected_player_rating:
                    return self.buy_player(player)
                else:
                    print("Found something, but rating (" + str(player_rating) + ") is not as expected (" + str(expected_player_rating) + ").")
                    return self.buy_player(player)
        return 0

    def buy_players(self, player, player_rating, max_price, max_player_count):
        try:
            self.go_to_transfer_market_search()
            sleep(random.randint(3, 9)/10)
            self.fill_transfer_search(player, max_price)
            sleep(random.randint(3, 9)/10)

            # begin
            count = 0
            success_count = 0
            coins = self.get_coins()
            print("Number of available coins: " + str(coins))
            print("Looking for " + player + " for max price " + str(max_price) + " coins...")

            while coins >= max_price and success_count < max_player_count:
                # Buy a player when result appears
                self.begin_transfer_market_search()
                price = self.try_buy_player(player, player_rating)
                if price > 0:
                    coins = self.get_coins()
                    success_count += 1
                self.end_transfer_market_search()

                if count % INCREASE_COUNT == 0:
                    self.reset_instant_buy_min_price(count)
                    count = 0
                else:
                    self.increase_instant_buy_min_price()

                count += 1
                sleep(random.randint(3, 9)/10)

        except TimeoutException:
            print("Error, check the browser")
