from django.db import models
from django.contrib.auth.models import User


class Collage(models.Model):
    """
    Collage model....
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    collage_description = models.CharField(max_length=300, blank=True)
    image = models.ImageField(
        upload_to='collage_images',
        default='../xPress/default_collage_image',
        blank=True
    )
    publish = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.title} by {self.owner}"
