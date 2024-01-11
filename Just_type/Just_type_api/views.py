from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .serializer import UserRegSerializer, UserLoginSerializer, UserErrorsSerializer
from .models import User_Errors
from .utils import Mongo_DB


class UserViewRegister(GenericAPIView):
    serializer_class = UserRegSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data = serializer.data

            user_id = serializer.data["id"]
            print("Дима сказал въебать сюда принты, гы: ", user_id)

            our_base = Mongo_DB()
            our_base.create_table_errors(user_id)
            print("Если всё збс, то ты видишь этот принт и тэйбл ин датабазе")

            return Response({
                'data': user_data,
                'message': 'thanks for signing up'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewLogin(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserErrorView(GenericAPIView):
    serializer_class = UserErrorsSerializer

    def post(self, request):

        user_id = request.data.get("userId", None)
        if not user_id:
            return Response({"error": "Method PUT not allowed"})

        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            our_base = Mongo_DB()
            our_base.update_user_errors(user_id, serializer.data["letters"])

            return Response(serializer.data, status=status.HTTP_200_OK)
        elif serializer.data["userId"] == '':
            return Response({"message": "NonAuthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
