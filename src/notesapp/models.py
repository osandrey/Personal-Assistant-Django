from django.db import models
from usersapp.models import CustomUser


class Tag(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class Note(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
