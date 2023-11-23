from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    model = User
    fields = ['username']
