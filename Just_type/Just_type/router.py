class JustTypeRouter:
    def db_for_read(self, model, **hints):
        """Выбирает нужную БД при реализации операции чтения."""
        if model._meta.model_name == "user":
            return 'default'
        elif model._meta.model_name == "All_Words" or "User_Errors":
            return 'just_type_mongodb'

        return None

    def db_for_write(self, model, **hints):
        """Выбирает нужную БД при реализации записи"""
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        """Определяет, могут ли две модели иметь отношение."""
        # Так как связи между разными базами данных в Django запрещены,
        # здесь требуется условие, запрещающее связи.
        if obj1._state.db in ['default', 'just_type_mongodb'] and \
           obj2._state.db in ['default', 'just_type_mongodb']:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Управляет миграциями моделей."""
        if db == 'default':
            # Указывается, что миграции для default БД разрешены только для определенных моделей
            return model_name in ['User']
        if db == 'just_type_mongodb':
            return model_name in ['All_Words', "User_Errors"]
        return None