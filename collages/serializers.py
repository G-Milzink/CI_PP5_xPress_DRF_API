from rest_framework import serializers
from .models import Collage
from likes.models import Like


class CollageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Collage database model.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(
        source='owner.profile.avatar.url'
    )
    like_id = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()
    likes_count = serializers.ReadOnlyField()

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 5:
            raise serializers.ValidationError(
                'Image size exceeds 5MB!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width exceeds 4096 pixels!'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height exceeds 4096 pixels!'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, collage=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Collage
        fields = [
            'id', 'owner', 'title',
            'collage_description',
            'created_on', 'updated_on',
            'profile_id', 'profile_image',
            'is_owner', 'like_id',
            'comments_count', 'likes_count',
            'publish',
        ]

        for i in range(1, 21):  # This generates fields for image1 to image20
            image_field_name = f'image{i}'
            fields.append(image_field_name)

        fields = list(set(fields))
