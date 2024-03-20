from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .serializer import *

from .utils import Errors


class UserViewRegister(GenericAPIView):
    serializer_class = UserRegSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data = serializer.data
            user_id = serializer.data["id"]
            # create table errors for user
            errors = Errors()
            errors.create_user_errors_record(user_id)

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

        global unique_words
        user_id = request.data.get("userId", None)
        count_words = request.data.get("count_words", None)
        if not user_id:
            return Response({"message": "NonAuthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            errors = Errors()
            errors.update_user_errors(user_id, serializer.data["letters"])

            user_errors = errors.get_user_errors(user_id)

            if user_errors:
                top_errors = errors.get_top_errors(user_errors)
                unique_words = errors.get_unique_words_by_errors(top_errors, count_words)
                print("Топовые ошибки пользователя:", top_errors)
                print("Уникальные слова по этим ошибкам:", unique_words)
                print(len(unique_words))
            else:
                print(f"Документ с user_id {user_id} не найден.")
            pass

            return Response({
                'errors_data': serializer.data,
                'message': f'Слова для пользователя {user_id} сгенерированны успешно',
                'unique_words': unique_words  # или можно возвратить None
            }, status=status.HTTP_200_OK)

        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    # Попробовать убрать pk = '', -> pk
    def get(self, request, pk='') -> Response:
        user_id = pk

        if not user_id:
            return Response({"message": "NonAuthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        error = Errors()
        user_errors = error.get_user_errors(user_id)

        if user_errors:
            return Response({
                'errors_data': user_errors,
                'message': f'Информация об ошибках {user_id} пользователя получена успешно',

            }, status=status.HTTP_200_OK)
        else:
            print(f"Документ с user_id {user_id} не найден.")
            return Response(user_errors.data, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        user_id = pk

        if not user_id:
            return Response({"message": "NonAuthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserErrorResetSerializer()

        try:
            errors = Errors()
            errors.reset_user_errors(user_id)
            return Response({
                'errors_data': serializer.data,
                'message': f'Слова для пользователя {user_id} удаленны успешно',

            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
