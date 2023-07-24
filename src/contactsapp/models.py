from django.db import models

from django.core.validators import RegexValidator
from django.contrib.postgres.fields import ArrayField
from datetime import datetime
from dateutil.relativedelta import relativedelta

"""To import top-level model from any app"""
from django.contrib.auth import get_user_model


class Contact(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(blank=False, max_length=255)
    last_name = models.CharField(blank=False, max_length=255)
    birth_date = models.DateField(blank=False)
    phone_regex = RegexValidator(r'^\d{5,15}$', 'Enter a valid phone number.'
                                                ' Min lenght is 5, max lenght is 15, only numbers.')
    phone_number = models.CharField(max_length=15, validators=[phone_regex])
    email = models.EmailField(blank=False)
    address = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sex = models.CharField(max_length=12, blank=False)
    status = models.CharField(max_length=12, blank=False)

