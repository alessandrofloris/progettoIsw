import time

from selenium.webdriver.common.by import By


def login(driver, user):
    username = user["username"]
    password = user["password"]

    login_username = driver.find_element(By.NAME, "username")
    login_username.clear()
    login_username.send_keys(username)

    login_password = driver.find_element(By.NAME, "password")
    login_password.send_keys(password)

    login_button = driver.find_element(By.NAME, "login_button")
    login_button.click()

    time.sleep(1)

def logout(driver):

    logout_button = driver.find_element(By.NAME, "logout_button")
    logout_button.click()

    time.sleep(1)
