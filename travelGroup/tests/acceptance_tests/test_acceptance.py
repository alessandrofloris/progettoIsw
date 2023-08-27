import time
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.edge.webdriver import WebDriver

from selenium.webdriver.common.by import By
from travelGroup.models import CustomUser, Trip, Invitation
from travelGroup.tests.acceptance_tests.ActivityTest import ActivityTest
from travelGroup.tests.acceptance_tests.AuthenticationTest import AuthenticationTest
from travelGroup.tests.acceptance_tests.CommentTest import CommentTest
from travelGroup.tests.acceptance_tests.TripTest import TripTest
from travelGroup.tests.acceptance_tests.InvitationTest import InvitationTest


class AcceptanceTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.user1_data = {'username': 'user1',
                           'password': 'password1',
                           'email': 'user_1@mail.com',
                           'first_name': 'name1',
                           'last_name': 'surname1'
                           }

        self.user2_data = {'username': 'user2',
                           'password': 'password2',
                           'email': 'user_2@mail.com',
                           'first_name': 'name2',
                           'last_name': 'surname2'
                           }

        self.trip1_data = {
            "name": "test_trip_name",
            "destination": "test_trip_destination",
            "departure_date": "2023-08-01",
            "arrival_date": "2023-08-10"
        }

        self.trip2_data = {
            "name": "test_trip_name2",
            "destination": "test_trip_destination2",
            "departure_date": "2023-09-01",
            "arrival_date": "2023-09-10"
        }

        self.activity_data = {
            "name": "test_trip_name2",
            "description": "test_trip_destination2",
            "start_date": "2023-08-06",
            "end_date": "2023-08-07"
        }

        # Crea gli utenti e i viaggi
        self.user1 = CustomUser.objects.create_user(**self.user1_data)
        self.user2 = CustomUser.objects.create_user(**self.user2_data)
        self.trip1 = Trip.objects.create(**self.trip1_data)
        self.trip2 = Trip.objects.create(**self.trip2_data)
        self.trip1.participants.add(self.user1)

        self.test_invitation = {
            "sender": self.user1,
            "recipient": self.user2_data["email"],
            "trip": self.trip1,
        }

        self.test_comment = {
            "content": "Commento di prova",
            "user": self.user2,
            "trip": self.trip2,
        }
        self.driver = WebDriver()

    def test_logout(self):
        self.driver.get(self.live_server_url)

        AuthenticationTest.login(self.driver, self.user1_data)
        AuthenticationTest.logout(self.driver)

        self.driver.quit()

    def from_mytrips_to_trip_detail(self, id):
        self.driver.find_element(By.NAME, "viewtrip").click()

    def test_show_trip_details(self):
        self.driver.get(self.live_server_url)
        AuthenticationTest.login(self.driver, self.user1_data)
        self.from_mytrips_to_trip_detail(self.trip1.id)
        trip_name = self.driver.find_element(By.ID, "detail-trip-name").text
        expected_content = self.trip1.name
        self.assertEqual(trip_name, expected_content)

    def test_there_are_no_trips(self):
        self.driver.get(self.live_server_url)
        AuthenticationTest.login(self.driver, self.user2_data)
        expected_content = "No trips to show!"
        content = self.driver.find_element(By.ID, "no-trips-title")

        self.assertEqual(content.text, expected_content)

    def test_there_are_trips(self):
        self.driver.get(self.live_server_url)
        AuthenticationTest.login(self.driver, self.user1_data)
        TripTest.create_trip(self, self.trip1_data)
        expected_content = "Your trips"
        content = self.driver.find_element(By.ID, "trips-title")

        self.assertEqual(content.text, expected_content)

    def test_there_are_n_trips(self):
        self.driver.get(self.live_server_url)
        AuthenticationTest.login(self.driver, self.user2_data)
        TripTest.create_trip(self, self.trip1_data)
        TripTest.create_trip(self, self.trip2_data)
        expected_result = 2
        content = self.driver.find_elements(By.CLASS_NAME, "single-trip-container")
        number_of_trips = len(content) - 1
        self.assertEqual(number_of_trips, expected_result)

    def test_login(self):
        self.driver.get(self.live_server_url)

        # Username wrong
        self.user1_data["username"] = "user_wrong"
        AuthenticationTest.login(self.driver, self.user1_data)
        time.sleep(2)

        # Password wrong
        self.user1_data["username"] = "user1"
        self.user1_data["password"] = "psw_wrong"
        AuthenticationTest.login(self.driver, self.user1_data)
        time.sleep(2)

        # Data set correctly
        self.user1_data["password"] = "password1"
        AuthenticationTest.login(self.driver, self.user1_data)

        self.driver.quit()

    def test_new_trip(self):
        self.driver.get(self.live_server_url)

        AuthenticationTest.login(self.driver, self.user1_data)

        # The start_date is set after end_date
        self.trip1_data["departure_date"] = "2023-08-10"
        self.trip1_data["arrival_date"] = "2023-08-01"
        TripTest.create_trip(self, self.trip1_data)
        time.sleep(2)

        # Data is set correctly
        self.trip1_data["departure_date"] = "2023-08-01"
        self.trip1_data["arrival_date"] = "2023-08-10"
        TripTest.create_trip(self, self.trip1_data)

        self.driver.quit()

    def test_new_activity(self):
        self.driver.get(self.live_server_url)

        AuthenticationTest.login(self.driver, self.user1_data)

        # Activity ends before start_date
        self.activity_data["end_date"] = "2023-07-10"
        ActivityTest.create_activity(self, self.trip1.id, self.activity_data)
        time.sleep(2)

        # Activity ends before trip end_date
        self.activity_data["end_date"] = "2023-08-11"
        ActivityTest.create_activity(self, self.trip1.id, self.activity_data)
        time.sleep(2)

        # Activity data set correctly
        self.activity_data["end_date"] = "2023-08-07"
        ActivityTest.create_activity(self, self.trip1.id, self.activity_data)

        self.driver.quit()

    def test_modify_trip(self):
        self.driver.get(self.live_server_url)

        AuthenticationTest.login(self.driver, self.user1_data)

        # The start_date is set after end_date
        self.trip1_data["departure_date"] = "2023-08-11"
        self.trip1_data["arrival_date"] = "2023-08-02"
        TripTest.modify_trip(self, self.trip1.id, self.trip1_data)

        # Data is set correctly
        self.trip1_data["departure_date"] = "2023-08-02"
        self.trip1_data["arrival_date"] = "2023-08-11"
        TripTest.modify_trip(self, self.trip1.id, self.trip1_data)

        self.driver.quit()

    def test_new_invitation(self):
        self.driver.get(self.live_server_url)

        AuthenticationTest.login(self.driver, self.user1_data)

        # Email not valid
        self.test_invitation["recipient"] = "non_valid_email@email.com"
        InvitationTest.new_invitation(self, self.test_invitation)
        time.sleep(2)

        # Valid invitation
        self.test_invitation["recipient"] = self.user2_data["email"]
        InvitationTest.new_invitation(self, self.test_invitation)
        time.sleep(2)

        # The user has already been invited
        InvitationTest.new_invitation(self, self.test_invitation)
        time.sleep(2)

        self.driver.quit()

    def test_view_trip(self):
        self.driver.get(self.live_server_url)

        AuthenticationTest.login(self.driver, self.user1_data)
        TripTest.view_trip(self, self.trip1.id)

        self.driver.quit()

    def test_accept_invitation(self):

        new_invitation = Invitation.objects.create(**self.test_invitation)

        self.driver.get(self.live_server_url)
        AuthenticationTest.login(self.driver, self.user2_data)

        InvitationTest.process_invitation(self, True)
        self.driver.quit()

    def test_decline_invitation(self):

        new_invitation = Invitation.objects.create(**self.test_invitation)

        self.driver.get(self.live_server_url)
        AuthenticationTest.login(self.driver, self.user2_data)

        InvitationTest.process_invitation(self, False)
        self.driver.get(self.live_server_url + "/invite")
        time.sleep(2)

        self.driver.quit()

    def test_add_comment(self):
        self.driver.get(self.live_server_url)
        AuthenticationTest.login(self.driver, self.user1_data)

        CommentTest.new_comment(self, self.test_comment)
        time.sleep(2)

        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
