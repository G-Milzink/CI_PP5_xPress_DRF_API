from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

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

    class Meta:
        model = Profile
        fields = [
            'id', 'owner',
            'name', 'avatar', 'bio',
            'created_on', 'updated_on',
            'is_owner'
        ]
