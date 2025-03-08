# profiles/tests/test_models.py

from django.test import TestCase
from django.contrib.auth.models import User
from ..models import UserProfile
import uuid

class UserProfileModelTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="testuser1", password="password123")
        self.user_profile1 = UserProfile.objects.create(
            user=self.user1,
            name="Test User 1",
            email="testuser1@example.com",
            username="testuser1",
            profession="Developer",
            about="Test profile about information"
        )

        # Ensure you're creating a new user for the second profile
        self.user2 = User.objects.create_user(username="testuser2", password="password123")
        self.user_profile2 = UserProfile.objects.create(
            user=self.user2,
            name="Test User 2",
            email="testuser2@example.com",
            username="testuser2",
            profession="Designer",
            about="Another profile about information"
        )

    def test_profile_id_is_unique(self):
        # Ensure the profile_id is unique by checking both profiles
        self.assertNotEqual(self.user_profile1.profile_id, self.user_profile2.profile_id)
