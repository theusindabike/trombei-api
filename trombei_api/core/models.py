from django.db import models


class File(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField()

    class Meta:
        abstract = True
