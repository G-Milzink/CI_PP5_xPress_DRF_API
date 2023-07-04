from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.usernam')

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'name', 'avatar', 'bio', 'created_on', 'updated_on'
        ]
