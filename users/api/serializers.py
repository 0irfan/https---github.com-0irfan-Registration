from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_admin = serializers.BooleanField(default=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'is_admin']

    def create(self, validated_data):
        is_admin = validated_data.pop('is_admin', False)
        is_staff=validated_data.pop('is_staff',False)
        try:
            if is_admin:
                user = CustomUser.objects.create_admin(**validated_data)
            elif is_staff and not is_admin:
                user = CustomUser.objects.create_staff(**validated_data)
            else:
                user=CustomUser.objects.create_user(**validated_data)
            return user
        except Exception as e:
            raise serializers.ValidationError(str(e))
