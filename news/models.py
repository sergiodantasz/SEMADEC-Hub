from django.db import models
from django.utils import timezone


class News(models.Model):
    administrator = models.ForeignKey(
        'users.Administrator',
        on_delete=models.SET_NULL,
        null=True,
        db_column='administrator_id',
    )
    title = models.CharField(
        max_length=200,
    )
    excerpt = models.CharField(
        max_length=200,
    )
    cover = models.ImageField(
        upload_to='',  # CHANGE IT LATER.
        default=None,
    )
    content = models.TextField()
    slug = models.SlugField(
        max_length=225,
        unique=True,
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
