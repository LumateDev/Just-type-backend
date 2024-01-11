from pymongo import MongoClient


class Mongo_DB():
    def __init__(self):
        # Подключение к MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['just_type']
        self.collection = db['Just_type_api_user_errors']

    def create_table_errors(self, user_id):
        user_document = {
            "user_id": user_id,
            "letters": {chr(i): 0 for i in range(ord('a'), ord('z') + 1)}
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


# Пример использования функции
"""db = Mongo_DB()
user_id = "ваш_id_пользователя"
error_updates = {"a": 3, "b": 1, "c": 2}
result = db.update_user_errors(user_id, error_updates)
print(f"Обновлено {result} документов")"""
