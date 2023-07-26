from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from profiles.models import Profile


class xpressAPIGlobalTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='user_a', password='pass_a')

    def test_creating_user_creates_profile(self):
        count = Profile.objects.count()
        response = self.client.get('/profiles/')
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deleting_user_deletes_profile(self):
        user = User.objects.get(username='user_a')
        user.delete()
        response = self.client.get('/profiles/1/')
        count = Profile.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
