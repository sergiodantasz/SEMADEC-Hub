from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from helpers.model import get_object
from helpers.slug import generate_dynamic_slug


class Course(models.Model):
    name = models.CharField(
        max_length=75,
        unique=True,
    )
    slug = models.SlugField(
        unique=True,
        max_length=100,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_dynamic_slug(self, 'name')
        reg = get_object(self.__class__, pk=self.pk)  # type: ignore
        if reg and self.name != reg.name:
            self.slug = generate_dynamic_slug(self, 'name')
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Class(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
    )
    entry_year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(3000),
        ],
    )
    slug = models.SlugField(
        max_length=45,
        unique=True,
    )
    course = models.ForeignKey(
        'teams.Course',
        on_delete=models.SET_NULL,
        null=True,
        db_column='course_id',
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_dynamic_slug(self, 'name')
        reg = get_object(self.__class__, pk=self.pk)  # type: ignore
        if reg and self.name != reg.name:
            self.slug = generate_dynamic_slug(self, 'name')
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)


class Team(models.Model):
    name = models.CharField(
        max_length=75,
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
    )
    classes = models.ManyToManyField(
        to='teams.Class',
        related_name='teams',
    )

    @property
    def get_classes(self):
        return self.classes.all()

    @property
    def get_editions(self):
        return self.editions.all()

    @property
    def get_edition_team(self):
        return self.edition_team.all()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_dynamic_slug(self, 'name')
        reg = get_object(self.__class__, pk=self.pk)  # type: ignore
        if reg and self.name != reg.name:
            self.slug = generate_dynamic_slug(self, 'name')
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
