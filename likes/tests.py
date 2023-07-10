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


class CommentDetailViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='user_a',
            password='pass_a'
        )
        User.objects.create_user(
            username='user_b',
            password='pass_b'
        )

    def test_can_retreive_like_with_valid_id(self):
        user_a = User.objects.get(username='user_a')
        post = Post.objects.create(owner=user_a, title='title_a')
        Like.objects.create(owner=user_a, post=post)
        response = self.client.get('/likes/1/')
        self.assertEqual(response.data['owner'], 'user_a')
        self.assertEqual(response.data['post'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_retreive_like_with_invalid_id(self):
        user_a = User.objects.get(username='user_a')
        post = Post.objects.create(owner=user_a, title='title_a')
        response = self.client.get('/likes/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_logged_in_user_can_remove_owned_like(self):
        user_a = User.objects.get(username='user_a')
        self.client.login(username='user_a', password='pass_a')
        post = Post.objects.create(owner=user_a, title='title_a')
        Like.objects.create(owner=user_a, post=post)
        response = self.client.delete('/likes/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logged_in_user_can_not_remove_unowned_like(self):
        user_a = User.objects.get(username='user_a')
        user_b = User.objects.get(username='user_b')
        self.client.login(username='user_b', password='pass_b')
        post = Post.objects.create(owner=user_a, title='title_a')
        Like.objects.create(owner=user_a, post=post)
        response = self.client.delete('/likes/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_out_user_can_not_remove_like(self):
        user_a = User.objects.get(username='user_a')
        post = Post.objects.create(owner=user_a, title='title_a')
        Like.objects.create(owner=user_a, post=post)
        self.client.logout()
        response = self.client.delete('/likes/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
