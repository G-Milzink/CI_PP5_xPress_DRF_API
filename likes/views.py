from rest_framework import generics, permissions
from xpress_api.permissions import IsOwnerOrReadOnly
from likes.models import Like
from .serializers import LikeSerializer
