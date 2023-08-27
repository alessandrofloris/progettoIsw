import unittest

from django.test import TestCase

from travelGroup.forms import InvitationForm
from travelGroup.models import Trip, CustomUser, Invitation


class InvitationTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # # Create two test users
        cls.test_user1 = CustomUser.objects.create(username='t1', email='t1@email.com')
        cls.test_user2 = CustomUser.objects.create(username='t2', email='t2@email.com')

        # Create a test trip and add test_user1 as a participant
        cls.test_trip = Trip.objects.create(
            name='test_trip_name',
            destination='test_trip_destination',
            departure_date='2023-08-01',
            arrival_date='2023-08-10',
        )
        cls.test_trip.participants.add(cls.test_user1)

    def test_email_validity(self):

        # Test the validity of an invitation form with a valid email
        form = InvitationForm(sender_user=self.test_user1,
                              data={'recipient_email': self.test_user2.email, 'trip': self.test_trip})
        self.assertTrue(form.is_valid())

        # The following email isn't stored in the db
        non_existing_email = 'non_existing_email@email.com'

        # Test the validity of an invitation form with a non-existing email
        form = InvitationForm(sender_user=self.test_user1,
                              data={'recipient_email': non_existing_email, 'trip': self.test_trip})
        self.assertFalse(form.is_valid())
        self.assertRaises(CustomUser.DoesNotExist, CustomUser.objects.get, email=non_existing_email)
        self.assertIn(form.ERROR_EMAIL_NOT_FOUND, form.errors['__all__'])

    def test_recipient_already_participating(self):

        # Test the validity of an invitation form with a recipient already participating
        form = InvitationForm(sender_user=self.test_user1,
                              data={'recipient_email': self.test_user1.email, 'trip': self.test_trip})
        self.assertFalse(form.is_valid())
        self.assertIn(self.test_user1, self.test_trip.participants.all())
        self.assertNotIn(self.test_user2, self.test_trip.participants.all())
        self.assertIn(form.ERROR_ALREADY_PARTICIPATING, form.errors['__all__'])


    def test_invitation_already_exists(self):
        # Test the validity of an invitation form with a duplicate invitation

        # Make an invitation from user1 to user2
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

        # Attempt to create another invitation for the same trip with the same recipient
        form = InvitationForm(sender_user=self.test_user1,
                              data={'recipient_email': self.test_user2.email, 'trip': self.test_trip})
        self.assertFalse(form.is_valid())
        self.assertNotIn(self.test_user2, self.test_trip.participants.all())
        self.assertEqual(inv, Invitation.objects.get(recipient=self.test_user2.email, trip=self.test_trip))
        self.assertIn(form.ERROR_INVITATION_EXISTS, form.errors['__all__'])


if __name__ == '__main__':
    unittest.main()
