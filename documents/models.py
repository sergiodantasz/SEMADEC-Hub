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
        unique=True,
        max_length=225,
    )
    created_at = models.DateTimeField(
        editable=False,
    )
    updated_at = models.DateTimeField(
        default=None,
    )
    tags = models.ManyToManyField(
        to='home.Tag',
    )

    def save(self, *args, **kwargs):
        if not self.id:  # type: ignore
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)
