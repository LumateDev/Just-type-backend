from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from .serializer import *
from .utils import Errors, Statics, Experience


class UserViewRegister(GenericAPIView):
    serializer_class = UserRegSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data = serializer.data
            user_id = serializer.data["id"]
            # create table errors, stats, experience  for user
            errors = Errors()
            statistics = Statics()
            experience = Experience()

            errors.create_user_errors_record(user_id)
            statistics.create_user_stats_record(user_id, 0, 0)
            experience.create_user_experience_record(user_id, 0)

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

    def get(self, request, pk) -> Response:

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
                'message': f'Ошибки для пользователя {user_id} удаленны успешно',

            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class UserDataView(GenericAPIView):
    serializer_class = UserDataSerializer

    def post(self, request):
        user_id = request.data.get("user_id", None)

        if not user_id:
            return Response({"message": "NonAuthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserDataSerializer(data=request.data)

        try:
            if serializer.is_valid():
                current_wpm = serializer.data['WPM']
                current_accuracy = serializer.data['accuracy']
                exp = serializer.data['experience']

                stats = Statics()
                stats.update_user_stats_record(user_id, current_wpm, current_accuracy)

                experience = Experience()
                experience.update_user_experience_record(user_id, exp)

                return Response({
                    'data': serializer.data,
                    'message': "Успешно 200 ок",

                }, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"sorry": "1"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk) -> Response:

        user_id = pk

        if not user_id:
            return Response({"message": "NonAuthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        stats = Statics()
        exp = Experience()
        user_stats = stats.get_user_stats(user_id)
        user_exp = exp.get_user_exp(user_id)
        threshold = exp.get_level_up_thresholds(current_level=user_exp.level+1)

        print(user_exp)
        print(user_stats)
        print(user_stats.__dict__.items())
        #print(dir(user_exp), user_exp.__dict__.items())


        if user_exp and user_stats:
            return Response({
                'data' : {'user_id': user_id,
                          'experience': user_exp.experience,
                          'level': user_exp.level,
                          'average_WPM': user_stats.average_WPM,
                          'average_accuracy': user_stats.average_accuracy,
                          'best_WPM': user_stats.best_WPM,
                          'best_accuracy': user_stats.best_accuracy,
                          'tests_count': user_stats.tests_count,
                          'threshold': threshold
                                                         },
                'message': f'Информация о статистике пользователя {user_id} получена успешно',

            }, status=status.HTTP_200_OK)
        else:

            return Response({user_stats.data, user_exp}, status=status.HTTP_400_BAD_REQUEST)
