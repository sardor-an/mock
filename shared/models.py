from django.db import models

from uuid import uuid4


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True