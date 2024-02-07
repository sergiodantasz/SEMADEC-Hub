from django.db import models
from django.utils import timezone


class Collection(models.Model):
    administrator = models.ForeignKey(
        'users.Administrator',
        on_delete=models.SET_NULL,
        null=True,
        db_column='administrator_id',
    )
    title = models.CharField(
        unique=True,
        max_length=200,
    )
    cover = models.ImageField(
        upload_to='',  # CHANGE IT LATER.
        default='/base/static/global/img/collection_cover_placeholder.jpg',  # REVIEW LATER
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


class File(models.Model):
    collection = models.ForeignKey(
        'archive.Collection',
        on_delete=models.CASCADE,
        db_column='collection_id',
    )
    content = models.FileField(
        unique=True,
        db_column='path',
    )
