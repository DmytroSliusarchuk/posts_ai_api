from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model with additional fields.
    """

    email = models.EmailField(unique=True)
    auto_response_enabled = models.BooleanField(default=False)
    auto_response_delay = models.IntegerField(default=5)

    def __str__(self):
        return self.username
