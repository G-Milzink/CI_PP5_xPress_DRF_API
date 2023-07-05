from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Post(models.Model):
    """
    Post database model.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    include_text = models.BooleanField(default=False)
    text = models.TextField(blank=True)
    excerpt = models.CharField(max_length=300, blank=True)
    include_image = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to='post_images',
        default='../xPress/default_post_image',
        blank=True
    )
    image_description = models.CharField(max_length=300, blank=True)
    include_audio = models.BooleanField(default=False)
    audio = CloudinaryField(
        folder='xPress/post_audios',
        resource_type='auto',
        blank=True
    )
    audio_description = models.CharField(max_length=300, blank=True)
    publish = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.title} by {self.owner}"
