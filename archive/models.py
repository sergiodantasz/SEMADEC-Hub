from django.db import models

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
    slug = models.CharField(
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


class CollectionTag(models.Model):
    ...


class File(models.Model):
    ...
