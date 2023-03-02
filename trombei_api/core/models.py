import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class File(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField()

    class Meta:
        abstract = True
