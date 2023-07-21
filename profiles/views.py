from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from xpress_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    """
    Lists all profiles
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_on')
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_on',
        'owner__followed__created_on',
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve a Profile, edit it if you are the owner.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_on')
