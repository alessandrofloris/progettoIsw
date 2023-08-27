import unittest
from django.test import Client

from django.test import TestCase

from django.urls import reverse
from travelGroup.models import Trip, CustomUser, Comment


class CommentTest(TestCase):

    def setUp(self):
        # Create a test client for HTTP requests
        self.client = Client()

        # Test user
        self.test_user1 = CustomUser.objects.create_user(username='t1', first_name='test', last_name='test',
                                                         email='t1@email.com', password='testpassword')
        # Log in the test user
        self.client.login(username='t1', password='testpassword')

        # Create a test trip
        self.test_trip = Trip.objects.create(
            name='test_trip_name',
            destination='test_trip_destination',
            departure_date='2023-08-01',
            arrival_date='2023-08-10',
        )

    def test_comment(self):
        # Add the test user as a participant in the test trip
        self.test_trip.participants.add(self.test_user1)

        comment_content = 'Test comment'

        # Prepare form data for a new comment
        form = {'content': comment_content}

        comment_count_before = Comment.objects.filter(trip=self.test_trip).count()

        # Post the comment and expect a redirection
        response = self.client.post(reverse('travelGroup:add_comment', args=[self.test_trip.id]), data=form)
        self.assertEqual(response.status_code, 302)  # correct redirect

        # Check if the comment was added correctly to the database
        comment_count_after = Comment.objects.filter(trip=self.test_trip).count()
        self.assertGreater(comment_count_after, comment_count_before)
        self.assertTrue(Comment.objects.filter(content=comment_content).exists())

        comment = Comment.objects.get(content=comment_content)
        self.assertEqual(comment.user, self.test_user1)
        self.assertEqual(comment.trip, self.test_trip)


if __name__ == '__main__':
    unittest.main()
