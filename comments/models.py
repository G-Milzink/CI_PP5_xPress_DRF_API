from django.db import models
from django.contrib.auth.models import User
from posts.models import Post
from collages.models import Collage


class Comment(models.Model):
    """
    Comment model,
    relates to User and Post models.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    collage = models.ForeignKey(
        Collage,
        on_delete=models.CASCADE,
        null=True,
        default=None
    )
    text = models.CharField(max_length=500, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']
