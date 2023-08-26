import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from travelGroup.models import CustomUser


class NewTripViewAcceptanceTest(StaticLiveServerTestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_superuser(username='testuser', first_name='test', last_name='user',
                                                        email='testemail@email.com', password='testpassword')
        self.user.save()
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get(self.live_server_url)

        login_username = self.driver.find_element(By.NAME, "username")
        login_username.send_keys("testuser")

        login_password = self.driver.find_element(By.NAME, "password")
        login_password.send_keys("testpassword")

        login_button = self.driver.find_element(By.NAME, "login_button")
        login_button.click()

    def home(self):
        newtrip_button = self.driver.find_element(By.NAME, "newtrip_button")
        newtrip_button.click()

    def create_trip(self):
        self.home()

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

        trip_create_button = self.driver.find_element(By.NAME, "create_button")
        trip_create_button.click()

    def test_there_are_no_trips(self):
        self.login()
        expected_content = "No trips to show!"
        content = self.driver.find_element(By.ID, "no-trips-title")

        self.assertEqual(content.text, expected_content)

    def test_there_are_trips(self):
        self.login()
        self.create_trip()
        expected_content = "Your trips"
        content = self.driver.find_element(By.ID, "trips-title")

        self.assertEqual(content.text, expected_content)

    def test_there_are_n_trips(self):
        self.login()
        self.create_trip()
        self.create_trip()

        expected_result = 2
        content = self.driver.find_elements(By.CLASS_NAME, "single-trip-container")
        number_of_trips = len(content) - 1
        self.assertEqual(number_of_trips, expected_result)
