from django.db import models

from helpers.model import get_object
from helpers.slug import generate_dynamic_slug


class News(models.Model):
    administrator = models.ForeignKey(
        'users.User',
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
        upload_to='news/covers',
    )
    content = models.TextField()  # Does it need to be tested?
    slug = models.SlugField(
        max_length=225,
        unique=True,
    )
    tags = models.ManyToManyField(
        to='home.Tag',
        related_name='news',
    )
    created_at = models.DateTimeField(
        editable=False,
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    @property
    def get_tags(self):
        return self.tags.all()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_dynamic_slug(self, 'title')
        news = get_object(self.__class__, id=self.id)  # type: ignore
        if news and self.title != news.title:
            self.slug = generate_dynamic_slug(self, 'title')
        return super().save(*args, **kwargs)
