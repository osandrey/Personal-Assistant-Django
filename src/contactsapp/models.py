from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    birthday = models.DateField(max_length=10, null=False)
    phone = models.CharField(max_length=13, null=False, unique=True)
    email = models.EmailField(null=False)
    address = models.CharField(max_length=255, null=False)
    information = models.TextField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.last_name