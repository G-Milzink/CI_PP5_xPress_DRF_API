from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Follower


class FollowerListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='user_a', password='pass_a')
        User.objects.create_user(username='user_b', password='pass_b')

    def test_can_list_followers(self):
        user_a = User.objects.get(username='user_a')
        user_b = User.objects.get(username='user_b')
        Follower.objects.create(owner=user_a, followed=user_b)
        response = self.client.get('/followers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_follow_other_user(self):
        self.client.login(username='user_a', password='pass_a')
        user_a = User.objects.get(username='user_a')
        user_b = User.objects.get(username='user_b')
        response = self.client.post(
            '/followers/', {'owner': user_a, 'followed': user_b.id}
        )
        count = Follower.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_can_not_follow_other_user(self):
        user_a = User.objects.get(username='user_a')
        user_b = User.objects.get(username='user_b')
        response = self.client.post(
            '/followers/', {'owner': user_a, 'followed': user_b}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
