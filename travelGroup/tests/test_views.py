from django.test import TestCase, Client
from django.urls import reverse
from travelGroup.models import Trip, CustomUser

# --- Test Visualizza Viaggi ---

# ++ Test della view ++

# test 1
# test no viaggi

# test 2
# test con solo viaggi a cui l'utente partecipa
# i viaggi a cui l'utente partecipa vengono mostrati

# test 3
# test con solo viaggi a cui l'utente non partecipa
# i viaggi a cui l'utente non partecipa non vengono mostrati

# test 4
# test con sia con viaggi a cui l'utente partecipa, sia con quelli in cui non partecipa
# vengono mostrati solamente i viaggi a cui l'utente partecipa


# --- New Trip View Tests ---
class NewTripViewTestCase(TestCase):

    # Set up the testing environment before each test method. 
    # Initializes a client for simulating HTTP requests.
    def setUp(self):
        self.client = Client()
        # test user creation
        self.user = CustomUser.objects.create_user(username='testuser', first_name='test', last_name='user', email='testemail@email.com', password='testpassword')


    # Test the creation of a new trip using the 'create' button in the new trip form.
    # After form submission, the user should be redirected to the 'mytrips' page.
    # Additionally, check that the created trip's details match the provided data.
    def test_create_trip_and_redirect_to_mytrips(self):
        data = {
            'name': 'My Trip',
            'destination': 'My Destination',
            'departure_date': '2023-08-01',
            'arrival_date': '2023-08-10',
            'create_button': True
        }

        # test user login
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('travelGroup:newtrip'), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('travelGroup:mytrips'))

        trip = Trip.objects.get(name='My Trip')
        self.assertEqual(trip.name, 'My Trip')
        self.assertEqual(trip.destination, 'My Destination')
        self.assertEqual(str(trip.departure_date), '2023-08-01')
        self.assertEqual(str(trip.arrival_date), '2023-08-10')
        self.assertIn(self.user, trip.participants.all())

    # Test the creation of a new trip using the 'create and add' button in the new trip form.
    # After form submission, the user should be redirected to the 'addactivity' page with the
    # newly created trip's ID in the URL. Additionally, verify the HTTP response status code.
    def test_create_trip_and_redirect_to_addactivity(self):
        data = {
            'id': '1',
            'name': 'My Trip',
            'destination': 'My Destination',
            'departure_date': '2023-08-01',
            'arrival_date': '2023-08-10',
            'create_add_button': True
        }

        response = self.client.post(reverse('travelGroup:newtrip'), data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'addactivity/' + data['id'])
