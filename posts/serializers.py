from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(
        source='owner.profile.avatar.url'
    )
    audio = serializers.SerializerMethodField()

    def get_audio(self, obj):
        if obj.audio:
            return obj.audio.url
        return None

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 5:
            raise serializers.ValidationError(
                'Image size exceeds 5MB!'
            )
        if value.width > 4096:
            raise serializers.ValidationError(
                'Image width exceeds 4096 pixels!'
            )
        if value.height > 4096:
            raise serializers.ValidationError(
                'Image height exceeds 4096 pixels!'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'title',
            'include_text', 'text', 'excerpt',
            'include_image', 'image', 'image_description',
            'include_audio', 'audio', 'audio_description',
            'created_on', 'updated_on',
            'profile_id', 'profile_image',
            'is_owner',
        ]
