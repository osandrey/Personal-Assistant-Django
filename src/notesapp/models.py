from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    tag_name = models.CharField(max_length=25, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='tag of username')
        ]

    def __str__(self):
        return self.tag_name


class Note(models.Model):
    title = models.CharField(max_length=150, null=False)
    description = models.CharField(max_length=500, null=False)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
