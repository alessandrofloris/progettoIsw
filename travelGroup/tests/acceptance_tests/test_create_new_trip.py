from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from travelGroup.models import CustomUser

class NewTripViewAcceptanceTest(LiveServerTestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', first_name='test', last_name='user', email='testemail@email.com', password='testpassword')
        self.driver = webdriver.Chrome()

    # button clicked: "create_button"
    def test_create_trip(self):
        self.driver.get("http://127.0.0.1:8000/newtrip")

        trip_name = self.driver.find_element(By.NAME, "name")
        trip_name.send_keys("Test Trip")

        trip_destination = self.driver.find_element(By.NAME, "destination")
        trip_destination.send_keys("Test Destination")

        trip_departure_date = self.driver.find_element(By.NAME, "departure_date")
        date_value = "2023-08-15"
        self.driver.execute_script("arguments[0].value = arguments[1]", trip_departure_date, date_value)

        trip_arrival_date = self.driver.find_element(By.NAME, "arrival_date")
        date_value = "2023-08-16"
        self.driver.execute_script("arguments[0].value = arguments[1]", trip_arrival_date, date_value)

        # TODO: add partecipant to trip
    
        trip_create_button = self.driver.find_element(By.NAME, "create_button")
        trip_create_button.click()

        # cmd input
        input("\nPress Enter to close the browser...")

    # button clicked: "create_add_button"
    def test_create_trip_and_add_activity(self):
        self.driver.get("http://127.0.0.1:8000/newtrip")

        trip_name = self.driver.find_element(By.NAME, "name")
        trip_name.send_keys("Test Trip")

        trip_destination = self.driver.find_element(By.NAME, "destination")
        trip_destination.send_keys("Test Destination")

        trip_departure_date = self.driver.find_element(By.NAME, "departure_date")
        date_value = "2023-08-15"
        self.driver.execute_script("arguments[0].value = arguments[1]", trip_departure_date, date_value)

        trip_arrival_date = self.driver.find_element(By.NAME, "arrival_date")
        date_value = "2023-08-16"
        self.driver.execute_script("arguments[0].value = arguments[1]", trip_arrival_date, date_value)

        # TODO: add partecipant to trip

        trip_create_button = self.driver.find_element(By.NAME, "create_add_button")
        trip_create_button.click()

        # cmd input
        input("\nPress Enter to close the browser...")

