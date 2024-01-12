from typing import List, Any

from pymongo import MongoClient


class Mongo_DB():
    def __init__(self):
        # Подключение к MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['just_type']
        self.collection = db['Just_type_api_user_errors']

    def create_table_errors(self, user_id):
        all_characters = [chr(i) for i in range(ord('a'), ord('z') + 1)]

        user_document = {
            "user_id": user_id,
            "letters": {char: 0 for char in all_characters}
        }
        # Вставка созданного документа
        result = self.collection.insert_one(user_document)
        # Возвращение идентификатора вставленного документа
        return result.inserted_id

    def update_user_errors(self, user_id, error_updates):
        # Подготовка данных для обновления
        update_data = {"$inc": {"letters." + key: value for key, value in error_updates.items()}}

        # Выполнение обновления
        result = self.collection.update_one({"user_id": user_id}, update_data)

        # Возвращение результата (например, количество обновленных документов)
        return result.modified_count

    def reset_user_errors(self, user_id):

        all_characters = [chr(i) for i in range(ord('a'), ord('z') + 1)]
        update_data = {"$set": {"letters": {char: 0 for char in all_characters}}}
        result = self.collection.update_one({"user_id": user_id}, update_data)

        # Возвращение результата (например, количество обновленных документов)
        return result.modified_count


# Пример использования функции
"""db = Mongo_DB()
user_id = "ваш_id_пользователя"
error_updates = {"a": 3, "b": 1, "c": 2}
result = db.update_user_errors(user_id, error_updates)
print(f"Обновлено {result} документов")"""


class Mongo_DB_Recommendation():

    def __init__(self):
        # Подключение к MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['just_type']
        self.collection_error = db['Just_type_api_user_errors']
        self.collection_all_words = db['Just_type_api_all_words']

    def get_user_errors(self, user_id):

        # Запрос на получение документа по user_id
        user_document = self.collection_error.find_one({"user_id": user_id})

        if user_document:
            # Получение словаря "letters"
            letters_dict = user_document.get("letters", {})
            return letters_dict
        else:
            print("ГДЕ ДОКУМЕНТ????")
            return None

    def get_top_errors(self, letters_dict, top_count=5):
        # Сортировка словаря по значениям
        sorted_letters = sorted(letters_dict.items(), key=lambda x: x[1], reverse=True)

        # Выбор топовых ошибок
        top_errors = dict(sorted_letters[:top_count])

        return top_errors

    def get_unique_words_by_errors(self, top_errors, count_words):
        # Подключение к MongoDB

        # Формирование списка букв из топовых ошибок
        error_letters = list(top_errors.keys())

        conditions = [{"letters." + key: {"$exists": True}} for key in error_letters]

        # Запрос в коллекцию "words_bank" по условиям для каждой буквы из top_errors
        words_documents = self.collection_all_words.find({"$and": conditions})

        # Составление списка уникальных слов
        unique_words: list[list[Any] | Any] = list(set(doc["word"] for doc in words_documents))

        if len(unique_words) < count_words:

            words_documents_additional = self.collection_all_words.find({"$or": conditions})
            words_documents_additional = [word for word in words_documents_additional if word not in unique_words]
            unique_words_additional = list(set(doc["word"] for doc in words_documents_additional))
            sliced_list = unique_words_additional[len(unique_words): count_words]
            print(f"Было добавленно {len(sliced_list)} слов, так как база слов недостаточно заполенена")

            for elem in sliced_list:
                unique_words.append(elem)

        elif len(unique_words) > count_words:
            unique_words = unique_words[:count_words]

        return unique_words

    # Пример использования функций

# rec = Mongo_DB_Recommendation()
# user_id = 64
# user_errors = rec.get_user_errors(user_id)
#
# if user_errors:
#     top_errors = rec.get_top_errors(user_errors)
#     unique_words = rec.get_unique_words_by_errors(top_errors, 100)
#
#     print("Топовые ошибки пользователя:", top_errors)
#
#     print("Уникальные слова по этим ошибкам:", unique_words)
#     print(len(unique_words))
#
# else:
#     print(f"Документ с user_id {user_id} не найден.")
