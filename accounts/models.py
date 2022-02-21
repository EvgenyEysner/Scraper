from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(('адрес электронной почты'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # email, password by default

    objects = CustomUserManager()

    def __str__(self):
        return self.email
