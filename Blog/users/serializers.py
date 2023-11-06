from rest_framework import serializers
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name')

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
