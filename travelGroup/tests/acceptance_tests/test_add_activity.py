from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from travelGroup.models import Trip

class AddActivityViewAcceptanceTest(LiveServerTestCase):

    def setUp(self):
        # test trip creation
        self.trip = Trip.objects.create(name='Test Trip', destination='Test Destination', departure_date='2023-08-01', arrival_date='2023-08-10')

        self.driver = webdriver.Chrome()

    def test_add_activity(self):
        self.driver.get("http://127.0.0.1:8000/addactivity/" + str(self.trip.id))

        activity_name = self.driver.find_element(By.NAME, "name")
        activity_name.send_keys("Test Activity")

        activity_description = self.driver.find_element(By.NAME, "description")
        activity_description.send_keys("Test Description")

        activity_start_date = self.driver.find_element(By.NAME, "start_date")
        date_value = "2023-08-02"
        self.driver.execute_script("arguments[0].value = arguments[1]", activity_start_date, date_value)

        activity_end_date = self.driver.find_element(By.NAME, "end_date")
        date_value = "2023-08-03"
        self.driver.execute_script("arguments[0].value = arguments[1]", activity_end_date, date_value)

        trip_create_button = self.driver.find_element(By.NAME, "add_activity")
        trip_create_button.click()

        # cmd input
        input("\nPress Enter to close the browser...")
