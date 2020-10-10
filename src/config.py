from selenium import webdriver
import platform


def create_driver():
    system = platform.system()

    if system == 'Darwin':
        path = 'chrome_mac/chromedriver'
    elif system == 'Linux':
        path = 'chrome_linux/chromedriver'
    else:
        raise OSError(f'Operating system {system} is not supported')

    driver = webdriver.Chrome(
        executable_path=path
    )

    driver.set_window_position(0, 0)
    driver.set_window_size(1920, 1080)

    return driver


URL = "https://www.ea.com/pl-pl/fifa/ultimate-team/web-app/"

USER = {
    "email": "your_email@example.com",
    "password": "your_password",
}

PLAYER = {
    "name": "Sterling",
    "cost": 100001,
}

ALLOW_NOTIFICATIONS = True
