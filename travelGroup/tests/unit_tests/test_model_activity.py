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

    def test_add_activity_to_trip(self):
        activity = Activity(id=1, name="Restaurant",
                            start_date=datetime.datetime(2023, 11, 19, 10, 8, 7, 127325, tzinfo=pytz.UTC),
                            end_date=datetime.datetime(2023, 11, 20, 10, 8, 7, 127325, tzinfo=pytz.UTC),
                            trip_id=self.trip.id)
        activity.save()
        self.assertIn(activity, self.trip.activity_set.all())

    def test_activity_dates_in_trip_date_range(self):
        activity = Activity(id=1, name="Restaurant",
                            start_date=datetime.datetime(2023, 10, 9, 10, 8, 7, 127325, tzinfo=pytz.UTC),
                            end_date=datetime.datetime(2023, 10, 10, 10, 8, 7, 127325, tzinfo=pytz.UTC),
                            trip_id=self.trip.id)
        activity.save()
        self.assertTrue(Activity.check_dates_is_inside_trip_date_range(activity))

    def test_activity_dates_not_in_trip_date_range(self):
        activity = Activity(id=1, name="Restaurant",
                            start_date=datetime.datetime(2023, 10, 4, 10, 8, 7, 127325, tzinfo=pytz.UTC),
                            end_date=datetime.datetime(2023, 10, 10, 10, 8, 7, 127325, tzinfo=pytz.UTC),
                            trip_id=self.trip.id)
        activity.save()
        self.assertFalse(Activity.check_dates_is_inside_trip_date_range(activity))
