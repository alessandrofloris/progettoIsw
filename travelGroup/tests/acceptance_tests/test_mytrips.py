from travelGroup.tests.acceptance_tests.AuthenticationTest import AuthenticationTest
from travelGroup.tests.acceptance_tests.TripTest import TripTest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from travelGroup.models import CustomUser, Trip


class ViewTripsAcceptanceTest(StaticLiveServerTestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_superuser(username='testuser', first_name='test', last_name='user',
                                                        email='testemail@email.com', password='testpassword')
        self.user.save()
        self.user_data = {'username': 'testuser',
                          'password': 'testpassword',
                          'email': 'testemail@email.com',
                          'first_name': 'test',
                          'last_name': 'user'
                          }
        self.trip_data = {
            "name": "test_trip_name",
            "destination": "test_trip_destination",
            "departure_date": "2023-08-01",
            "arrival_date": "2023-08-10"
        }
        self.trip = Trip.objects.create(**self.trip_data)
        self.driver = webdriver.Chrome()

    def test_there_are_no_trips(self):
        self.driver.get(self.live_server_url)
        AuthenticationTest.login(self.driver, self.user_data)
        expected_content = "No trips to show!"
        content = self.driver.find_element(By.ID, "no-trips-title")

        self.assertEqual(content.text, expected_content)

    def test_there_are_trips(self):
        self.driver.get(self.live_server_url)
        AuthenticationTest.login(self.driver, self.user_data)
        TripTest.create_trip(self, self.trip_data)
        expected_content = "Your trips"
        content = self.driver.find_element(By.ID, "trips-title")

        self.assertEqual(content.text, expected_content)

    def test_there_are_n_trips(self):
        self.driver.get(self.live_server_url)
        AuthenticationTest.login(self.driver, self.user_data)
        TripTest.create_trip(self, self.trip_data)
        TripTest.create_trip(self, self.trip_data)

        expected_result = 2
        content = self.driver.find_elements(By.CLASS_NAME, "single-trip-container")
        number_of_trips = len(content) - 1
        self.assertEqual(number_of_trips, expected_result)
