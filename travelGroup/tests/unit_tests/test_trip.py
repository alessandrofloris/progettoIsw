from django.test import TestCase, Client
from django.urls import reverse
from travelGroup.models import Trip, CustomUser, Activity
from travelGroup.forms import ActivityForm


# --- New Trip View Tests ---
class TripTestCase(TestCase):

    # Set up the testing environment before each test method. 
    # Initializes a client for simulating HTTP requests.
    def setUp(self):
        self.client = Client()
        # test user creation
        self.user = CustomUser.objects.create_user(username='testuser', first_name='test', last_name='user', email='testemail@email.com', password='testpassword')
        # test user login
        self.client.login(username='testuser', password='testpassword')

        self.trip = Trip.objects.create(name='My Trip', destination='My Destination', departure_date='2023-08-07', arrival_date='2023-08-08')
        self.trip.participants.add(self.user)

    # Test the creation of a new trip using the 'create' button in the new trip form.
    # After form submission, the user should be redirected to the 'mytrips' page.
    # Additionally, check that the created trip's details match the provided data.
    def test_create_trip_and_redirect_to_mytrips(self):
        # new trip
        valid_data_trip = {
            'id': 2,
            'name': 'My Trip 1',
            'destination': 'My Destination 1',
            'departure_date': '2023-08-01',
            'arrival_date': '2023-08-10'
        }

        response = self.client.post(reverse('travelGroup:newtrip'), valid_data_trip)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('travelGroup:mytrips'))

        trip = Trip.objects.get(id=2)
        self.assertEqual(trip.name, 'My Trip 1')
        self.assertEqual(trip.destination, 'My Destination 1')
        self.assertEqual(str(trip.departure_date), '2023-08-01')
        self.assertEqual(str(trip.arrival_date), '2023-08-10')
        self.assertIn(self.user, trip.participants.all())

    # Test the creation of a new trip with the incorrect dates using 
    # the 'create' button in the new trip form.
    # After form submission, the user should remain in the "new trip" page 
    # with an error message displayed.
    def test_create_trip_with_arrival_date_less_than_departure_date(self):
        invalid_data_trip = {
            'name': 'My Trip',
            'destination': 'My Destination',
            'departure_date': '2023-08-10',
            'arrival_date': '2023-08-05'
        }

        response = self.client.post(reverse('travelGroup:newtrip'), invalid_data_trip)

        self.assertEqual(response.status_code, 200)
        # check for form validation error message
        self.assertContains(response, 'Departure date must be before the arrival date.')

    def test_modify_trip(self):
        new_data_trip = {
            'name': 'My Trip 2',
            'destination': 'My Destination 2',
            'departure_date': '2023-08-06',
            'arrival_date': '2023-08-09'
        }

        response = self.client.post(reverse('travelGroup:modifytrip', args=[self.trip.id]), new_data_trip)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('travelGroup:mytrips'))
        trip = Trip.objects.get(id=self.trip.id)
        self.assertEqual(trip.name, 'My Trip 2')
        self.assertEqual(trip.destination, 'My Destination 2')
        self.assertEqual(str(trip.departure_date), '2023-08-06')
        self.assertEqual(str(trip.arrival_date), '2023-08-09')
        self.assertIn(self.user, trip.participants.all())

