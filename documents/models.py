from django.db import models


class Document(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        db_column='user_id',
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

    def __str__(self):
        return str(self.title)