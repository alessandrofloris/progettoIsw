import datetime

from travelGroup.tests.acceptance_tests.AuthenticationTest import AuthenticationTest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from travelGroup.models import CustomUser, Trip


class TripDetailsAcceptanceTest(StaticLiveServerTestCase):

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

        self.trip_1 = Trip(id=1, name="Winter23", destination="Mallorca", departure_date=datetime.date(2023, 10, 5),
                           arrival_date=datetime.date(2023, 10, 20))
        self.trip_1.save()
        self.trip_1.participants.add(self.user)
        self.trip_1.save()

        self.driver = webdriver.Chrome()

    def from_mytrips_to_trip_detail(self, id):
        self.driver.find_element(By.NAME, "viewtrip").click()

    def test_show_trip_details(self):
        self.driver.get(self.live_server_url)
        AuthenticationTest.login(self.driver, self.user_data)
        self.from_mytrips_to_trip_detail(1)
        trip_name = self.driver.find_element(By.ID, "detail-trip-name").text
        expected_content = "Winter23"
        self.assertEqual(trip_name, expected_content)
