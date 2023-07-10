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


class CommentDetailViewTests(APITestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(
            username='user_a', password='pass_a')
        self.user_b = User.objects.create_user(
            username='user_b', password='pass_b')
        self.post = Post.objects.create(owner=self.user_a, title='title_a')

    def test_user_can_retrieve_comment_with_valid_id(self):
        Comment.objects.create(
            owner=self.user_a,
            post=self.post,
            text='text_a'
        )
        response = self.client.get('/comments/1')
        self.assertEqual(response.data['text'], 'text_a')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_not_retrieve_comment_with_invalid_id(self):
        Comment.objects.create(
            owner=self.user_a,
            post=self.post,
            text='text_a'
        )
        response = self.client.get('/comments/999')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_owned_comment(self):
        self.client.login(username='user_a', password='pass_a')
        Comment.objects.create(
            owner=self.user_a,
            post=self.post,
            text='text_a'
        )
        response = self.client.put('/comments/1', {'text': 'new_text'})
        comment = Comment.objects.filter(pk=1).first()
        self.assertEqual(comment.text, 'new_text')

    def test_user_can_not_update_unowned_comment(self):
        self.client.login(username='user_a', password='pass_a')
        Comment.objects.create(
            owner=self.user_b,
            post=self.post,
            text='text_a'
        )
        response = self.client.put('/comments/1', {'text': 'new_text'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_owned_comment(self):
        self.client.login(username='user_a', password='pass_a')
        Comment.objects.create(
            owner=self.user_a,
            post=self.post,
            text='text_a'
        )
        response = self.client.delete('/comments/1')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_can_not_delete_unowned_comment(self):
        self.client.login(username='user_a', password='pass_a')
        Comment.objects.create(
            owner=self.user_b,
            post=self.post,
            text='text_a'
        )
        response = self.client.delete('/comments/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
