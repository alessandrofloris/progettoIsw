from selenium.webdriver.common.by import By


def login(driver, url, username, password):
    driver.get(url)

    login_username = driver.find_element(By.NAME, "username")
    login_username.send_keys(username)

    login_password = driver.find_element(By.NAME, "password")
    login_password.send_keys(password)

    login_button = driver.find_element(By.NAME, "login_button")
    login_button.click()


def home(driver):
    newtrip_button = driver.find_element(By.NAME, "newtrip_button")
    newtrip_button.click()


def create_trip(driver):
    home(driver)

    trip_name = driver.find_element(By.NAME, "name")
    trip_name.send_keys("Test Trip")

    trip_destination = driver.find_element(By.NAME, "destination")
    trip_destination.send_keys("Test Destination")

    trip_departure_date = driver.find_element(By.NAME, "departure_date")
    date_value = "2023-08-15"
    driver.execute_script("arguments[0].value = arguments[1]", trip_departure_date, date_value)

    trip_arrival_date = driver.find_element(By.NAME, "arrival_date")
    date_value = "2023-08-16"
    driver.execute_script("arguments[0].value = arguments[1]", trip_arrival_date, date_value)

    trip_create_button = driver.find_element(By.NAME, "create_button")
    trip_create_button.click()