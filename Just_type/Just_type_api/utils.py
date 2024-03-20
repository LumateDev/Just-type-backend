from .models import User_Errors, User, All_Words, User_Data, User_Experience
import json

class Errors:
    def create_user_errors_record(self, user_id):
        user = User.objects.get(pk=user_id)
        all_characters = [chr(i) for i in range(ord('a'), ord('z') + 1)]
        letters_dict = {char: 0 for char in all_characters}
        User_Errors.objects.create(user_id=user, letters=letters_dict)

    def update_user_errors(self, user_id, error_updates):
        user_error = User_Errors.objects.get_or_create(user_id=user_id)[0]
        letters = user_error.letters
        for key, value in error_updates.items():
            letters[key] += value
        user_error.save()

    def reset_user_errors(self, user_id):
        all_characters = [chr(i) for i in range(ord('a'), ord('z') + 1)]
        user_error = User_Errors.objects.get_or_create(user_id=user_id)[0]
        user_error.letters = {char: 0 for char in all_characters}
        user_error.save()

    def get_user_errors(self, user_id):
        user_error = User_Errors.objects.filter(user_id=user_id).first()
        if user_error:
            return user_error.letters
        else:
            print("No document found")
            return None

    def get_top_errors(self, letters_dict, top_count=5):
        sorted_letters = sorted(letters_dict.items(), key=lambda x: x[1], reverse=True)
        top_errors = dict(sorted_letters[:top_count])
        return top_errors

    def get_unique_words_by_errors(self, top_errors, count_words):

        error_letters = list(top_errors.keys())
        conditions = {"letters__" + key + "__isnull": False for key in error_letters}
        words_documents = All_Words.objects.filter(**conditions)
        unique_words = set(doc.word for doc in words_documents)

        if len(unique_words) < count_words:
            additional_words = All_Words.objects.exclude(word__in=unique_words)
            additional_unique_words = set()
            for word in additional_words:
                letters_count = word.letters
                contains_top_error = any(letter in top_errors for letter in letters_count.keys())
                if contains_top_error:
                    additional_unique_words.add(word.word)

            unique_words.update(additional_unique_words)
        unique_words = list(unique_words)[:count_words]
        return unique_words


class Statics:
    def create_user_stats_record(self, user_id):
        user_data = User_Data(user_id_id=user_id, bestWPM=0, averageWPM=0, total_tests=0)
        user_data.save()


class Experience:
    def create_user_experience_record(self, user_id):
        user_experience = User_Experience(user_id_id=user_id, experience=0, level=0)
        user_experience.save()
