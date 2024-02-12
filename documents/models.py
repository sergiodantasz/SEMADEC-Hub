from django.db import models
from django.utils import timezone


class Document(models.Model):
    administrator = models.ForeignKey(
        'users.Administrator',
        on_delete=models.SET_NULL,
        null=True,
        db_column='administrator_id',
    )
    title = models.CharField(
        max_length=200,
    )
    content = models.FileField(
        unique=True,
        db_column='path',
    )
    slug = models.SlugField(
        max_length=225,
        unique=True,
    )
    created_at = models.DateTimeField(
        editable=False,
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
