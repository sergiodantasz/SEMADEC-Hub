from django.db import models


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
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return str(self.title)


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

    def __str__(self):
        return str(self.content.name)
