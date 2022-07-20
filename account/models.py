from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    permission_level = models.PositiveIntegerField(default=0)
