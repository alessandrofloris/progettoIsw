from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from travelGroup.models import CustomUser


class NewTripCreationAcceptanceTest(LiveServerTestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', first_name='test', last_name='user', email='testemail@email.com', password='testpassword')
        self.driver = webdriver.Chrome()

    def test_create_trip(self):
        trip_name = self.driver.find_element(By.NAME, "name")
        trip_name.send_keys("Test Trip")
        trip_destination = self.driver.find_element(By.NAME, "destination")
        trip_destination.send_keys("Test Destination")
        trip_departure_date = self.driver.find_element(By.NAME, "departure_date")
        trip_departure_date.send_keys("2023-07-10")
        trip_arrival_date = self.driver.find_element(By.NAME, "arrival_date")
        trip_arrival_date.send_keys("2023-07-15")



