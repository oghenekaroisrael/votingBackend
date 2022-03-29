from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'last_name',
            'first_name',
            'sex',
            'email',
            'password',
            'image_url',
            'face_id'
,            'NiN',
            'phoneNumber',
            'user_type',
            'activatedBy',
            'createdAt'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

        def create(self, validated_data):
            password = validated_data.pop('password', None)
            instance = self.Meta.model(**validated_data)
            if password is not None:
                instance.set_password(password)

            instance.save()
            return instance
