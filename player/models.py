from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


class Player(AbstractUser):
    USERNAME_FIELD = 'username'

    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, null=True)
    is_in_game = models.SmallIntegerField(default=0)

    def set_password(self, password):
        self.password = make_password(password)
