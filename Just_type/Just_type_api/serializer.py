from rest_framework import serializers
from .models import User
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
            raise AuthenticationFailed("Неверный пароль")
        if not user.is_active:
            raise AuthenticationFailed("unactive")

        return {
            'username': user.username,
            'id': user.id,

        }


class UserErrorsSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    letters = serializers.JSONField()
    count_words = serializers.IntegerField(write_only=True)

    class Meta:
        fields = ['userId', 'letters', 'count_words']


class UserErrorResetSerializer(serializers.Serializer):
    letters = serializers.JSONField(read_only=True)

    class Meta:
        fields = ['letters']


class UserDataSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    experience = serializers.FloatField()
    WPM = serializers.FloatField()
    accuracy = serializers.FloatField()
    tests_count = serializers.FloatField(read_only=True)

    class Meta:
        fields = ['user_id', 'experience', 'WPM', 'accuracy', 'test_count']
