from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='user_a', password='pass_a')

    def test_can_list_posts(self):
        user_a = User.objects.get(username='user_a')
        Post.objects.create(owner=user_a, title='title_a')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='user_a', password='pass_a')
        response = self.client.post('/posts/', {'title': 'title_a'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_can_not_create_post(self):
        response = self.client.post('/posts/', {'title': 'title_a'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        user_a = User.objects.create_user(username='user_a', password='pass_a')
        user_b = User.objects.create_user(username='user_b', password='pass_b')
        Post.objects.create(
            owner=user_a, title='title_a', text='text_a'
        )
        Post.objects.create(
            owner=user_b, title='title_b', text='text_b'
        )

    def test_user_can_retreive_post_with_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'title_a')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_not_retreive_post_with_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_owned_post(self):
        self.client.login(username='user_a', password='pass_a')
        response = self.client.put('/posts/1/', {'title': 'new_title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'new_title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_not_update_unowned_post(self):
        self.client.login(username='user_a', password='pass_a')
        response = self.client.put('/posts/2/', {'title': 'new_title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
