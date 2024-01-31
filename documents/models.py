from django.db import models
from django.utils import timezone

from home.models import Tag
from users.models import Administrator


class Document(models.Model):
    administrator = models.ForeignKey(
        Administrator,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        db_column='administrator_id',
    )
    title = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )
    content = models.FileField(
        unique=True,
        null=False,
        blank=False,
        db_column='path',
    )
    slug = models.SlugField(
        unique=True,
        max_length=225,
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(
        null=False,
        blank=False,
        editable=False,
    )
    updated_at = models.DateTimeField(
        blank=False,
        default=None,
    )
    # Add ManyToManyField into Tag model

    def save(self, *args, **kwargs):
        if not self.id:  # type: ignore
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)
