from django.db import models

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
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
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
