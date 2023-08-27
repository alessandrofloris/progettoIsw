import unittest

from django.test import TestCase

from travelGroup.forms import InvitationForm
from travelGroup.models import Trip, CustomUser, Invitation


class InvitationTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # first test user
        cls.test_user1 = CustomUser.objects.create(username='t1', email='t1@email.com')

        # second test user
        cls.test_user2 = CustomUser.objects.create(username='t2', email='t2@email.com')

        # create a test trip and add the test user as a participant
        cls.test_trip = Trip.objects.create(
            name='test_trip_name',
            destination='test_trip_destination',
            departure_date='2023-08-01',
            arrival_date='2023-08-10',
        )

    def test_email_validity(self):
        # Add the test user as a participant in the test trip
        self.test_trip.participants.add(self.test_user1)

        form = InvitationForm(sender_user=self.test_user1,
                              data={'recipient_email': self.test_user2.email, 'trip': self.test_trip})
        self.assertTrue(form.is_valid())

        # The following email isn't stored in the db
        non_existing_email = 'non_existing_email@email.com'

        form = InvitationForm(sender_user=self.test_user1,
                              data={'recipient_email': non_existing_email, 'trip': self.test_trip})
        self.assertFalse(form.is_valid())
        self.assertIn(form.ERROR_EMAIL_NOT_FOUND, form.errors['__all__'])

    def test_recipient_already_participating(self):
        # Add the test user as a participant in the test trip
        self.test_trip.participants.add(self.test_user1)

        form = InvitationForm(sender_user=self.test_user1,
                              data={'recipient_email': self.test_user2.email, 'trip': self.test_trip})
        self.assertTrue(form.is_valid())

        form = InvitationForm(sender_user=self.test_user1,
                              data={'recipient_email': self.test_user1.email, 'trip': self.test_trip})
        self.assertFalse(form.is_valid())
        self.assertIn(form.ERROR_ALREADY_PARTICIPATING, form.errors['__all__'])

    def test_invitation_already_exists(self):

        # Add the test user as a participant in the test trip
        self.test_trip.participants.add(self.test_user1)

        # make an identical invitation again
        form = InvitationForm(sender_user=self.test_user1,
                              data={'recipient_email': self.test_user2.email, 'trip': self.test_trip})
        self.assertTrue(form.is_valid())

        # Save the invitation on db
        inv = Invitation.objects.create(
            sender=self.test_user1,
            recipient=self.test_user2.email,
            trip=self.test_trip
        )
        inv.save()

        # remake another invitation for the same trip
        form = InvitationForm(sender_user=self.test_user1,
                              data={'recipient_email': self.test_user2.email, 'trip': self.test_trip})
        self.assertFalse(form.is_valid())
        self.assertIn(form.ERROR_INVITATION_EXISTS, form.errors['__all__'])


if __name__ == '__main__':
    unittest.main()
