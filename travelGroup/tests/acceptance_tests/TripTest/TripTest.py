import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def create_trip(self, trip):
    trip_name = trip["name"]
    trip_destination = trip["destination"]
    trip_departure_date = trip["departure_date"]
    trip_arrival_date = trip["arrival_date"]

    self.driver.get(self.live_server_url + "/newtrip")

    name_field = self.driver.find_element(By.NAME, "name")
    name_field.send_keys(trip_name)

    destination_field = self.driver.find_element(By.NAME, "destination")
    destination_field.send_keys(trip_destination)

    departure_date_field = self.driver.find_element(By.NAME, "departure_date")
    date_value = trip_departure_date
    self.driver.execute_script("arguments[0].value = arguments[1]", departure_date_field, date_value)

    arrival_date_field = self.driver.find_element(By.NAME, "arrival_date")
    date_value = trip_arrival_date
    self.driver.execute_script("arguments[0].value = arguments[1]", arrival_date_field, date_value)

    trip_create_button = self.driver.find_element(By.NAME, "create_button")
    time.sleep(2)
    trip_create_button.click()
    time.sleep(2)


def modify_trip(self, trip_id, trip):
    trip_name = trip["name"]
    trip_destination = trip["destination"]
    trip_departure_date = trip["departure_date"]
    trip_arrival_date = trip["arrival_date"]

    url = self.live_server_url + "/modifytrip/" + str(trip_id)
    self.driver.get(url)

    name_field = self.driver.find_element(By.NAME, "name")
    name_field.clear()
    name_field.send_keys(trip_name)

    destination_field = self.driver.find_element(By.NAME, "destination")
    destination_field.clear()
    destination_field.send_keys(trip_destination)

    departure_date_field = self.driver.find_element(By.NAME, "departure_date")
    date_value = trip_departure_date
    self.driver.execute_script("arguments[0].value = arguments[1]", departure_date_field, date_value)

    arrival_date_field = self.driver.find_element(By.NAME, "arrival_date")
    date_value = trip_arrival_date
    self.driver.execute_script("arguments[0].value = arguments[1]", arrival_date_field, date_value)

    trip_modify_button = self.driver.find_element(By.NAME, "modify_button")
    time.sleep(2)
    trip_modify_button.click()
    time.sleep(2)


def view_trip(self, trip_id):
    url = self.live_server_url + "/viewtrip/" + str(trip_id)
    self.driver.get(url)

    time.sleep(2)
