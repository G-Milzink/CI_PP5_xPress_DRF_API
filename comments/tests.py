from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from posts.models import Post
from .models import Comment


class CommentListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='user_a', password='pass_a')

    def test_can_list_comments(self):
        user_a = User.objects.get(username='user_a')
        post = Post.objects.create(owner=user_a, title='title_a')
        Comment.objects.create(owner=user_a, post=post, text='text_a')
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_comment(self):
        user_a = User.objects.get(username='user_a')
        self.client.login(username='user_a', password='pass_a')
        post = Post.objects.create(owner=user_a, title='title_a')
        response = self.client.post(
            '/comments/', {'text': 'text_a', 'post': post.id}
        )
        count = Comment.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_can_not_create_comment(self):
        user_a = User.objects.get(username='user_a')
        post = Post.objects.create(owner=user_a, title='title_a')
        response = self.client.post(
            '/comments/', {'text': 'text_a', 'post': post.id}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
