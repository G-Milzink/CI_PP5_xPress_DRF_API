from django.db.models import Count
from django.db.models.functions import Greatest
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from xpress_api.permissions import IsOwnerOrReadOnly
from .models import Collage
from .serializers import CollageSerializer


class CollageList(generics.ListCreateAPIView):
    """
    List all collages, create collage if logged in.
    """
    serializer_class = CollageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Collage.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by(Greatest('created_on', 'updated_on').desc())
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_on',
    ]
    search_fields = [
        'owner__username',
        'title',
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
