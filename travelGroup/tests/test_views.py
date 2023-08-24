from django.test import TestCase, Client
from django.urls import reverse
from travelGroup.models import Trip, CustomUser, Activity
from travelGroup.forms import ActivityForm

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
        # test user login
        self.client.login(username='testuser', password='testpassword')

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

        trip = Trip.objects.get(name='My Trip')
        self.assertEqual(trip.name, 'My Trip')
        self.assertEqual(trip.destination, 'My Destination')
        self.assertEqual(str(trip.departure_date), '2023-08-01')
        self.assertEqual(str(trip.arrival_date), '2023-08-10')
        self.assertIn(self.user, trip.participants.all())
    
    # Test the creation of a new trip with the incorrect dates using 
    # the 'create' button in the new trip form.
    # After form submission, the user should remain in the "new trip" page 
    # with an error message displayed.
    def test_create_trip_with_arrival_date_less_than_departure_date(self):
        data = {
            'id': '1',
            'name': 'My Trip',
            'destination': 'My Destination',
            'departure_date': '2023-08-10',
            'arrival_date': '2023-08-05',
            'create_button': True
        }

        response = self.client.post(reverse('travelGroup:newtrip'), data)

        self.assertEqual(response.status_code, 200)
        # check for form validation error message
        self.assertContains(response, 'Departure date must be before the arrival date.')

    # Test the creation of a new trip with the incorrect dates using 
    # the 'create and add' button in the new trip form.
    # After form submission, the user should remain in the "new trip" page 
    # with an error message displayed.  
    def test_create_and_add_activity_trip_with_arrival_date_less_than_departure_date(self):
        data = {
            'id': '1',
            'name': 'My Trip',
            'destination': 'My Destination',
            'departure_date': '2023-08-10',
            'arrival_date': '2023-08-05',
            'create_add_button': True
        }

        response = self.client.post(reverse('travelGroup:newtrip'), data)

        self.assertEqual(response.status_code, 200)
        # check for form validation error message
        self.assertContains(response, 'Departure date must be before the arrival date.')

        


# --- Add Activity View Tests ---
class AddActivityViewTestCase(TestCase):

    # Set up the testing environment before each test method. 
    # Initializes a client for simulating HTTP requests.
    def setUp(self):
        self.client = Client()
        # test user creation
        self.user = CustomUser.objects.create_user(username='testuser', first_name='test', last_name='user', email='testemail@email.com', password='testpassword')
        # test user login
        self.client.login(username='testuser', password='testpassword')
        # test trip creation
        self.trip = Trip.objects.create(name='Test Trip', destination='Test Destination', departure_date='2023-08-01', arrival_date='2023-08-10')

    # Test the behavior of the 'addactivity' view when a GET request is made.
    # This method simulates a GET request to the 'addactivity' view with a specific trip ID.
    # It checks whether the response status code is 200 (OK), verifies that the correct template
    # 'travelGroup/addactivity.html' is used for rendering the response, and ensures that the
    # context contains an instance of the ActivityForm.
    def test_addactivity_view_get_request(self):
        response = self.client.get(reverse('travelGroup:addactivity', args=[self.trip.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'travelGroup/addactivity.html')
        self.assertIsInstance(response.context['addActivityForm'], ActivityForm)

    # Test the behavior of the 'addactivity' view when a valid POST request is made.
    # This method simulates a POST request to the 'addactivity' view with valid form data.
    # It checks whether the response status code is 302 (redirect), verifies that the
    # redirection is correct using the assertRedirects method, and ensures that an Activity
    # instance is correctly created in the database with the provided data.
    def test_addactivity_view_post_valid_form(self):
        data = {
            'trip': self.trip,
            'name': 'Test Activity',
            'description': 'Test Description',
            'start_date': '2023-08-05',
            'end_date': '2023-08-06',
        }

        response = self.client.post(reverse('travelGroup:addactivity', args=[self.trip.id]), data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('travelGroup:mytrips'))

        activity = Activity.objects.get(name='Test Activity')
        self.assertEqual(activity.trip, self.trip)
        self.assertEqual(activity.description, 'Test Description')
        self.assertEqual(str(activity.start_date), '2023-08-05 00:00:00+00:00')
        self.assertEqual(str(activity.end_date), '2023-08-06 00:00:00+00:00')

    # Test the behavior of the 'addactivity' view when an invalid POST request is made.
    # This method simulates a POST request to the 'addactivity' view with invalid form data.
    # It checks whether the response status code is 200 (OK), verifies that the correct
    # template is used for rendering, ensures that the context contains an instance of the
    # ActivityForm with validation errors, and confirms that the response content contains
    # the expected form validation error message.
    def test_addactivity_view_post_invalid_form(self):
        # simulate an invalid form submission by not providing required fields
        data = {}

        response = self.client.post(reverse('travelGroup:addactivity', args=[self.trip.id]), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'travelGroup/addactivity.html')
        self.assertIsInstance(response.context['addActivityForm'], ActivityForm)
        # check for form validation error message
        self.assertContains(response, 'This field is required.')
    
    # Test the creation of a new activity with the incorrect dates.
    # After form submission, the user should remain in the "add activity" page 
    # with an error message displayed.
    def test_add_activity_with_end_date_less_than_start_date(self):
        data = {
            'trip': self.trip,
            'name': 'Test Activity',
            'description': 'Test Description',
            'start_date': '2023-08-10',
            'end_date': '2023-08-05',
        }

        response = self.client.post(reverse('travelGroup:addactivity', args=[self.trip.id]), data=data)

        self.assertEqual(response.status_code, 200)
        # check for form validation error message
        self.assertContains(response, 'Start date must be before the end date.')
