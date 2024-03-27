from .models import UserErrors, User, AllWords, UserData, UserExperience


class Errors:
    def create_user_errors_record(self, user_id):
        user = User.objects.get(pk=user_id)
        all_characters = [chr(i) for i in range(ord('a'), ord('z') + 1)]
        letters_dict = {char: 0 for char in all_characters}
        UserErrors.objects.create(user_id=user, letters=letters_dict)

    def update_user_errors(self, user_id, error_updates):
        user_error = UserErrors.objects.get_or_create(user_id=user_id)[0]
        letters = user_error.letters
        for key, value in error_updates.items():
            letters[key] += value
        user_error.save()

    def reset_user_errors(self, user_id):
        all_characters = [chr(i) for i in range(ord('a'), ord('z') + 1)]
        user_error = UserErrors.objects.get_or_create(user_id=user_id)[0]
        user_error.letters = {char: 0 for char in all_characters}
        user_error.save()

    def get_user_errors(self, user_id):
        user_error = UserErrors.objects.filter(user_id=user_id).first()
        return user_error.letters

    def get_top_errors(self, letters_dict, top_count=5):
        sorted_letters = sorted(letters_dict.items(), key=lambda x: x[1], reverse=True)
        top_errors = dict(sorted_letters[:top_count])
        return top_errors

    def get_unique_words_by_errors(self, top_errors, count_words):

        error_letters = list(top_errors.keys())
        conditions = {"letters__" + key + "__isnull": False for key in error_letters}
        words_documents = AllWords.objects.filter(**conditions)
        unique_words = set(doc.word for doc in words_documents)

        if len(unique_words) < count_words:
            additional_words = AllWords.objects.exclude(word__in=unique_words)
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
    def get_user_stats(self, user_id):
        user_stats = UserData.objects.filter(user_id=user_id).first()
        return user_stats

    def create_user_stats_record(self, user_id, current_wpm, current_accuracy):
        user_data = UserData(user_id_id=user_id, best_WPM=current_wpm, average_WPM=current_wpm,
                             average_accuracy=current_accuracy, best_accuracy=current_accuracy, tests_count=0)
        user_data.save()

    def update_user_stats_record(self, user_id, wpm, accuracy):

        data = UserData.objects.get(pk=user_id)

        if data.tests_count == 0:
            data.average_WPM = wpm
            data.best_WPM = wpm
            data.average_accuracy = accuracy
            data.best_accuracy = accuracy

        else:

            average_wpm = (data.average_WPM * data.tests_count + wpm) / (data.tests_count + 1)
            data.average_WPM = average_wpm
            data.best_WPM = max(data.best_WPM, wpm)

            average_accuracy = (data.average_accuracy * data.tests_count + accuracy) / (data.tests_count + 1)
            data.average_accuracy = average_accuracy
            data.best_accuracy = max(data.best_accuracy, accuracy)

        data.tests_count += 1

        print(f"Tests : {data.tests_count}")
        data.save()


class Experience:

    def get_level_up_thresholds(self, current_level):
        return 100 * (current_level ** 1.5)

    def get_user_exp(self, user_id):
        user_exp = UserExperience.objects.filter(user_id=user_id).first()
        return user_exp

    def create_user_experience_record(self, user_id, exp):
        user_experience = UserExperience(user_id_id=user_id, experience=exp, level=0)
        user_experience.save()

    def update_user_experience_record(self, user_id, exp):
        user_experience = UserExperience.objects.get(pk=user_id)

        user_experience.experience += exp
        threshold = self.get_level_up_thresholds(user_experience.level+1)
        print("Для перехода нужно: ", threshold)
        print("У нас есть ", user_experience.experience)
        if user_experience.experience >= threshold:

            user_experience.level += 1
            print("Level up!!", user_experience.level)
        user_experience.save()
