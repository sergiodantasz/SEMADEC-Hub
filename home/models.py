from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
    )
    slug = models.CharField(
        max_length=75,
        unique=True,
        null=False,
        blank=False,
    )
