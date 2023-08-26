import datetime
from django.test import TestCase
from travelGroup.models import Trip, CustomUser, Activity
import pytz


class TripTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser(username='testuser', first_name='test', last_name='user', email='testemail@email.com', password='testpassword')
        self.user.save()
        self.trip = Trip(id=1, name="Winter", departure_date=datetime.date(2023, 10, 5), arrival_date=datetime.date(2023, 10, 20))
        self.trip.save()

    def test_trip_creation(self):
        trip = Trip(id=1,name="Winter")
        expected_name = "Winter"
        self.assertEqual(trip.name, expected_name)

    def test_return_date_before_departure_date(self):
        departure_date = datetime.date(2023, 10, 5)
        return_date = datetime.date(2023, 10, 1)
        trip = Trip(id=1, name="Winter", departure_date=departure_date, arrival_date=return_date)
        self.assertFalse(Trip.check_dates(trip))

    def test_return_date_after_departure_date(self):
        departure_date = datetime.date(2023, 10, 5)
        return_date = datetime.date(2023, 10, 10)
        trip = Trip(id=1, name="Winter", departure_date=departure_date, arrival_date=return_date)
        self.assertTrue(Trip.check_dates(trip))

    def test_trip_add_participant(self):
        self.trip.participants.add(self.user)
        self.assertIn(self.user, self.trip.participants.all())
