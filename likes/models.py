from django.db import models
from django.contrib.auth.models import User
from posts.models import Post
from collages.models import Collage


class Like(models.Model):
    """
    Like model,
    relates to User and Post models.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name='likes', on_delete=models.CASCADE
    )
    collage = models.ForeignKey(
        Collage,
        related_name='likes',
        on_delete=models.CASCADE,
        null=True,
        default=None
    )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
        unique_together = ['owner', 'post', 'collage']

    def __str__(self):
        return f"{self.owner} {post}"
