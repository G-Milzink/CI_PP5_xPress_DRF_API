from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from posts.models import Post
from .models import Like


class LikeListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='user_a',
            password='pass_a'
        )
        User.objects.create_user(
            username='user_b',
            password='pass_b'
        )

    def test_can_list_likes(self):
        user_a = User.objects.get(username='user_a')
        post = Post.objects.create(owner=user_a, title='title_a')
        Like.objects.create(owner=user_a, post=post)
        response = self.client.get('/likes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_like_post(self):
        self.client.login(username='user_a', password='pass_a')
        user_a = User.objects.get(username='user_a')
        post = Post.objects.create(owner=user_a, title='title_a')
        response = self.client.post(
            '/likes/', {'owner': user_a, 'post': post.id})
        count = Like.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_can_not_like_post(self):
        self.client.logout()
        user_a = User.objects.get(username='user_a')
        post = Post.objects.create(owner=user_a, title='title_a')
        response = self.client.post(
            '/likes/', {'owner': user_a, 'post': post.id})
        count = Like.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
