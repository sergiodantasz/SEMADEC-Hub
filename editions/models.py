from django.db import models


class Course(models.Model):
    name = models.CharField(
        unique=True,
        max_length=75,
        null=False,
        blank=False,
    )


class Edition(models.Model):
    ...
