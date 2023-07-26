from rest_framework import serializers
from .models import Profile
from followers.models import Follower


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile model
    Adds 'is_owner', 'following_id', 'posts_count',,
    'followers_count' and 'following_count' fields
    on retreival of profiles list.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    def validate_avatar(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size exceeds 2MB!'
            )
        if value.width > 1024:
            raise serializers.ValidationError(
                'Image width exceeds 1024 pixels!'
            )
        if value.height > 4096:
            raise serializers.ValidationError(
                'Image height exceeds 1024 pixels!'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    class Meta:
        model = Profile
        fields = [
            'id', 'owner',
            'name', 'avatar', 'bio',
            'created_on', 'updated_on',
            'is_owner', 'following_id',
            'posts_count', 'followers_count', 'following_count',
        ]
