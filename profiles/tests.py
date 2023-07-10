from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Profile


class ProfileListViewTests(APITestCase):

    def test_can_list_profiles(self):
        User.objects.create_user(username='user_a', password='pass_a')
        count = Profile.objects.count()
        response = self.client.get('/profiles/')
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileDetailViewTests(APITestCase):

    def test_can_retreive_profile_with_valid_id(self):
        User.objects.create_user(username='user_a', password='pass_a')
        response = self.client.get('/profiles/1/')
        self.assertEqual(response.data['owner'], 'user_a')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_retreive_profile_with_invalid_id(self):
        User.objects.create_user(username='user_a', password='pass_a')
        response = self.client.get('/profiles/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_logged_in_user_can_update_owned_profile(self):
        User.objects.create_user(username='user_a', password='pass_a')
        self.client.login(username='user_a', password='pass_a')
        response = self.client.put('/profiles/1/', {'name': 'new_name'})
        self.assertEqual(response.data['name'], 'new_name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_not_update_unowned_profile(self):
        User.objects.create_user(username='user_a', password='pass_a')
        User.objects.create_user(username='user_b', password='pass_b')
        self.client.login(username='user_a', password='pass_a')
        response = self.client.put('/profiles/2/', {'name': 'new_name'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_user_can_not_update_unowned_profile(self):
        User.objects.create_user(username='user_a', password='pass_a')
        self.client.logout()
        response = self.client.put('/profiles/1/', {'name': 'new_name'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
