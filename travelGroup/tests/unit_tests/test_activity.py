from django.test import TestCase, Client
from django.urls import reverse
from travelGroup.models import Trip, CustomUser, Activity
from travelGroup.forms import ActivityForm


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

    # Test the creation of a new activity whit its dates within the trip dates.
    # After form submission, it checks whether the response status code is 302 (redirect), and 
    # verifies that the redirection is correct using the assertRedirects method.
    def test_activity_dates_range_within_trip_dates(self):
        data = {
            'trip': self.trip,
            'name': 'Test Activity',
            'description': 'Test Description',
            'start_date': '2023-08-02',
            'end_date': '2023-08-05',
        }

        response = self.client.post(reverse('travelGroup:addactivity', args=[self.trip.id]), data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('travelGroup:mytrips'))

    # Test the creation of a new activity with the start date outside the trip dates range.
    # After form submission, it checks whether the response status code is 302 (redirect), and 
    # verifies that the redirection is correct using the assertRedirects method.
    def test_activity_start_date_outside_range_trip_dates(self):
        data = {
            'trip': self.trip,
            'name': 'Test Activity',
            'description': 'Test Description',
            'start_date': '2023-07-02', # less than trip's departure date
            'end_date': '2023-08-09',
        }

        response = self.client.post(reverse('travelGroup:addactivity', args=[self.trip.id]), data=data)

        self.assertEqual(response.status_code, 200)
        # check for form validation error message
        self.assertContains(response, "Activity dates must be within the trip dates range.")

    # Test the creation of a new activity with the end date outside the trip dates range.
    # After form submission, it checks whether the response status code is 302 (redirect), and 
    # verifies that the redirection is correct using the assertRedirects method.
    def test_activity_end_date_outside_range_trip_dates(self):
        data = {
            'trip': self.trip,
            'name': 'Test Activity',
            'description': 'Test Description',
            'start_date': '2023-08-02',
            'end_date': '2023-08-11', # greater than trip's arrival date
        }

        response = self.client.post(reverse('travelGroup:addactivity', args=[self.trip.id]), data=data)

        self.assertEqual(response.status_code, 200)
        # check for form validation error message
        self.assertContains(response, "Activity dates must be within the trip dates range.")
