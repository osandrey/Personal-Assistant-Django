from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(models.Model):
    email = models.EmailField(blank=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator]
    )
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(blank=True, default=None)
    avatar = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
