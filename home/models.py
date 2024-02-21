from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(
        max_length=75,
        unique=True,
    )
    news = models.ManyToManyField(
        to='news.News',
        related_name='tags',
    )
    collection = models.ManyToManyField(
        to='archive.Collection',
        related_name='tags',
    )
    document = models.ManyToManyField(
        to='documents.Document',
        related_name='tags',
    )

    def __str__(self):
        return str(self.name)
