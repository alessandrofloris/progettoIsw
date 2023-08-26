from selenium.webdriver.common.by import By
import time


def login(driver, url, username, password):

    driver.get(url)

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(username)
    password_input.send_keys(password)

    time.sleep(4)

    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
