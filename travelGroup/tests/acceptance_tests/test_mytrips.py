from . import utils
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from travelGroup.models import CustomUser


class ViewTripsAcceptanceTest(StaticLiveServerTestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_superuser(username='testuser', first_name='test', last_name='user',
                                                        email='testemail@email.com', password='testpassword')
        self.user.save()
        self.driver = webdriver.Chrome()

    def test_there_are_no_trips(self):
        utils.login(self.driver, self.live_server_url, "testuser", "testpassword")
        expected_content = "No trips to show!"
        content = self.driver.find_element(By.ID, "no-trips-title")

        self.assertEqual(content.text, expected_content)

    def test_there_are_trips(self):
        utils.login(self.driver, self.live_server_url, "testuser", "testpassword")
        utils.create_trip(self.driver)
        expected_content = "Your trips"
        content = self.driver.find_element(By.ID, "trips-title")

        self.assertEqual(content.text, expected_content)

    def test_there_are_n_trips(self):
        utils.login(self.driver, self.live_server_url, "testuser", "testpassword")
        utils.create_trip(self.driver)
        utils.create_trip(self.driver)

        expected_result = 2
        content = self.driver.find_elements(By.CLASS_NAME, "single-trip-container")
        number_of_trips = len(content) - 1
        self.assertEqual(number_of_trips, expected_result)
