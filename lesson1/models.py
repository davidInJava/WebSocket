from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from .managers import UserManager
import jwt
# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(max_length=120, null=False, unique=True)
    email = models.EmailField(unique=True, null=True)
    role = models.CharField(max_length=120, default='user')
    password = models.CharField(max_length=120, null=False)
    objects = UserManager()
    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['role']
    def __str__(self):
        return self.nickname +' '+ self.email
    @property
    def token(self):
            return self._generate_jwt_token()

    def _generate_jwt_token(self):

        dt = datetime.now() + timedelta(days=60 )

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.timestamp() , # Используем метод timestamp(),
            'nickname': self.nickname,
        }, settings.SECRET_KEY, algorithm='HS256')

        return token