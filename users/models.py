import jwt

from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.core import validators
from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin
from .managers import AppUserManager
# Create your models here.

class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name = 'Email address',
        max_length = 255,
        validators = (validators.validate_email,),
        unique = True,
        blank = False
    )

    first_name = models.CharField(
        verbose_name = 'First name',
        max_length = 255,
    )

    last_name = models.CharField(
        verbose_name = 'Last name',
        max_length = 255,
    )

    is_active = models.BooleanField(
        verbose_name = 'Is active',
        default=True,
    )

    is_admin = models.BooleanField(
        verbose_name = 'Is admin',
        default=False,
    )

    created = models.DateTimeField(
        verbose_name = "Created",
        auto_now_add = True,
    )

    updated = models.DateTimeField(
        verbose_name = "Updated",
        auto_now = True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'first_name',
        'last_name',
    )

    objects = AppUserManager()

    class Meta:

        verbose_name = "AppUser"
        verbose_name_plural = "AppUsers"
        ordering = ('-created',)

    def __str__(self):
        return '%s' % self.email
    
    @property
    def is_staff(self):
        return self.is_admin

    @property
    def token(self):
        """
        Позволяет нам получить токен пользователя, вызвав `user.token` вместо
        `user.generate_jwt_token().

        Декоратор `@property` выше делает это возможным.
        `token` называется «динамическим свойством ».
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей,
        как обработка электронной почты.
        Обычно это имя и фамилия пользователя.
        Поскольку мы не храним настоящее имя пользователя,
        мы возвращаем его имя пользователя.
        """
        return ("%s %s") % (self.first_name, self.last_name)

    def get_short_name(self):
        """
        Этот метод требуется Django для таких вещей,
        как обработка электронной почты.
        Как правило, это будет имя пользователя.
        Поскольку мы не храним настоящее имя пользователя,
        мы возвращаем его имя пользователя.
        """
        return ("%s") % (self.first_name)

    def _generate_jwt_token(self):
        """
        Создает веб-токен JSON, в котором хранится идентификатор
        этого пользователя и срок его действия
        составляет 30 дней в будущем.
        """
        dt = datetime.now() + timedelta(days=30)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')