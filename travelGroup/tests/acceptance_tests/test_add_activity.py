from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from travelGroup.models import CustomUser

class AddActivityViewAcceptanceTest(StaticLiveServerTestCase):

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

    # button clicked: "create_add_button"
    def create_trip(self):

        trip_name = self.driver.find_element(By.NAME, "name")
        trip_name.send_keys("Test Trip")

        trip_destination = self.driver.find_element(By.NAME, "destination")
        trip_destination.send_keys("Test Destination")

        trip_departure_date = self.driver.find_element(By.NAME, "departure_date")
        date_value = "2023-08-10"
        self.driver.execute_script("arguments[0].value = arguments[1]", trip_departure_date, date_value)

        trip_arrival_date = self.driver.find_element(By.NAME, "arrival_date")
        date_value = "2023-08-16"
        self.driver.execute_script("arguments[0].value = arguments[1]", trip_arrival_date, date_value)

        trip_create_button = self.driver.find_element(By.NAME, "create_button")
        trip_create_button.click()

    def test_add_activity(self):

        self.login()
        self.home()
        self.create_trip()

        addactivity_link = self.driver.find_element(By.NAME, "addactivity")
        addactivity_link.click()

        activity_name = self.driver.find_element(By.NAME, "name")
        activity_name.send_keys("Test Activity")

        activity_description = self.driver.find_element(By.NAME, "description")
        activity_description.send_keys("Test Description")

        activity_start_date = self.driver.find_element(By.NAME, "start_date")
        date_value = "2023-08-11"
        self.driver.execute_script("arguments[0].value = arguments[1]", activity_start_date, date_value)

        activity_end_date = self.driver.find_element(By.NAME, "end_date")
        date_value = "2023-08-12"
        self.driver.execute_script("arguments[0].value = arguments[1]", activity_end_date, date_value)

        trip_create_button = self.driver.find_element(By.NAME, "add_activity")
        trip_create_button.click()

