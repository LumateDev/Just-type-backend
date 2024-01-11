from rest_framework import serializers
from .models import User, User_Errors, All_Words
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class UserRegSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, min_length=8, write_only=True)
    repeat_password = serializers.CharField(max_length=100, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeat_password', 'id']

    def validate(self, attrs):
        password = attrs.get('password', '')
        repeat_password = attrs.get('repeat_password', '')
        if password != repeat_password:
            raise serializers.ValidationError("passwords do not match")

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            username=validated_data.get('username'),
            password=validated_data.get('password')
        )

        return user


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, min_length=6)
    password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'id']

    def validate(self, attrs):
        username = attrs.get('username', None)
        password = attrs.get('password', None)
        request = self.context.get('request')
        user = authenticate(request, username=username, password=password)
        if not user:
            raise AuthenticationFailed("invalid")
        if not user.is_active:
            raise AuthenticationFailed("unactive")

        return {
            'username': user.username,
            'id': user.id,

        }


class UserErrorsSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField()
    letters = serializers.JSONField()

    class Meta:
        model = User_Errors
        fields = ['userId', 'letters']

    def update(self, instance, validated_data):
        instance.userId = validated_data.get("userId", instance.userId)
        instance.letters = validated_data.get("letters", instance.letters)

        instance.save()
        return instance
