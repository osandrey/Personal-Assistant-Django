from django.db import models

from django.core.validators import RegexValidator
from django.contrib.postgres.fields import ArrayField
from datetime import datetime
from dateutil.relativedelta import relativedelta

from usersapp.models import CustomUser


class Contact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField(blank=True, null=True, default=None)
    phone_regex = RegexValidator(r'^\d{5,15}$', 'Enter a valid phone number.'
                                                ' Min lenght is 5, max lenght is 15, only numbers.')
    phone_number = ArrayField(models.CharField(max_length=15, validators=[phone_regex]))
    email = ArrayField(models.EmailField(blank=True))
    address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, default=None)
    updated_at = models.DateTimeField(blank=True, default=None)
    MALE = "male"
    FEMALE = "female"
    GENDER = [
        (MALE, "male"),
        (FEMALE, "female"),
    ]
    sex = models.CharField(
        max_length=6,
        choices=GENDER,
    )
    FAMILY = "family"
    FRIEND = "friend"
    PARTNER = "partner"
    COLLEAGUE = "colleague"
    OTHER = "other"
    STATUSES = [
        (FAMILY, "family"),
        (FRIEND, "friend"),
        (PARTNER, "partner"),
        (COLLEAGUE, "colleague"),
        (OTHER, "other")
    ]
    status = models.CharField(
        max_length=9,
        choices=STATUSES,
    )

    @property
    def age(self):
        age_delta = relativedelta(datetime.utcnow(), self.birth_date)
        return age_delta.years

