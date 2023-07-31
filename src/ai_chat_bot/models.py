from django.db import models

# Create your models here.
class TelegramUsers(models.Model):

    custom_user_id = models.CharField()
    telegram_user_id = models.CharField(unique=True)

