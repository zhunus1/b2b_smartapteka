from django.contrib.auth.models import BaseUserManager

class AppUserManager(BaseUserManager):
    """
    Django требует, чтобы пользовательские `User`
    определяли свой собственный класс Manager.
    Унаследовав от BaseUserManager, мы получаем много кода,
    используемого Django для создания `User`.

    Все, что нам нужно сделать, это переопределить функцию
    `create_user`, которую мы будем использовать
    для создания объектов `User`.
    """

    def _create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Данный адрес электронной почты должен быть установлен')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Создает и возвращает `User` с адресом электронной почты,
        именем пользователя и паролем.
        """
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, first_name, last_name, password, **extra_fields)

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        """
        Создает и возвращает пользователя с правами
        суперпользователя (администратора).
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Суперпользователь должен иметь is_admin=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(email, first_name, last_name, password, **extra_fields)