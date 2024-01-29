from django.db import models

from news.models import News
from users.models import Administrator


class Collection(models.Model):
    administrator = models.ForeignKey(
        Administrator,
        on_delete=models.SET_NULL,
        blank=False,
        db_column='administrator_id',
    )
    title = models.CharField(
        unique=True,
        max_length=200,
        null=False,
        blank=False,
    )
    cover = models.ImageField(
        upload_to='',  # Change it later
        null=False,
        blank=True,  # Can it be blank?
    )
    slug = models.SlugField(
        unique=True,
        max_length=225,
        null=False,
        blank=False,
    )
    creation_date = models.DateField(
        null=False,
        blank=True,  # Can it be blank?
    )
    update_date = models.DateField(
        null=False,
        blank=True,  # Can it be blank?
    )
    # Add ManyToManyField into Tag model


class File(models.Model):
    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,  # Delete file when its collection is deleted
        blank=False,
        db_column='collection_id',
    )
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
    )
    size = models.PositiveBigIntegerField(  # Is this file type correct?
        null=False,
        blank=False,
    )
