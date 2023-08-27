from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from travelGroup.models import CustomUser


class NewTripViewAcceptanceTest(StaticLiveServerTestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_superuser(username='testuser', first_name='test', last_name='user', email='testemail@email.com', password='testpassword')
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

    # button clicked: "create_button"
    def test_create_trip(self):

        self.login()
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

    # button clicked: "create_add_button"
    def test_create_trip_and_add_activity(self):

        self.login()
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
    