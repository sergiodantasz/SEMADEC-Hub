from django.db import models

from helpers.model import get_object
from helpers.slug import generate_dynamic_slug


class Category(models.Model):
    name = models.CharField(
        primary_key=True,
        max_length=15,
    )

    @property
    def get_css_class(self):
        classes = {
            'Masculino': 'category-tag-male',
            'Feminino': 'category-tag-female',
            'Misto': 'category-tag-mix',
        }
        return (
            classes.get(self.name) or 'category-tag-undefined'
        )  # Add undefined css class later

    def __str__(self):
        return str(self.name)


class Sport(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
    )
    slug = models.SlugField(
        max_length=225,
        unique=True,
    )
    categories = models.ManyToManyField(
        to='competitions.Category',
        through='competitions.SportCategory',
        related_name='sports',
    )

    @property
    def get_categories(self):
        return self.categories.all()

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_dynamic_slug(self, 'name')
        reg = get_object(self.__class__, pk=self.id)  # type: ignore
        if reg and self.name != reg.name:
            self.slug = generate_dynamic_slug(self, 'name')
        return super().save(*args, **kwargs)


class SportCategory(models.Model):
    sport = models.ForeignKey(
        'competitions.Sport',
        related_name='sport_category',
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        'competitions.Category',
        related_name='sport_category',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.sport.name} - {self.category.name}'


class Match(models.Model):
    sport_category = models.ForeignKey(
        'competitions.SportCategory',
        related_name='matches',
        on_delete=models.CASCADE,
    )
    edition = models.ForeignKey(
        'editions.Edition',
        on_delete=models.CASCADE,
    )
    teams = models.ManyToManyField(
        to='editions.Team',
        through='competitions.MatchTeam',
        related_name='matches',
    )
    scoreboard = models.CharField(max_length=10)  # Change later
    date_time = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return str(self.sport.name)


class MatchTeam(models.Model):
    match = models.ForeignKey(
        'competitions.Match',
        on_delete=models.CASCADE,
    )
    team = models.ForeignKey(
        'editions.Team',
        on_delete=models.CASCADE,
    )
    score = models.FloatField(
        null=True,
        blank=True,
        default=0,
    )
    winner = models.BooleanField()

    def __str__(self):
        return str(self.team.name)


class Test(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True,  # I think it should have unique constraint
    )
    slug = models.SlugField(
        max_length=225,
        unique=True,
    )
    # Add edition field??
    description = models.TextField(
        null=True,
        blank=True,
        default='',
    )
    date_time = models.DateTimeField(
        default=None,
    )
    teams = models.ManyToManyField(
        to='editions.Team',
        through='competitions.TestTeam',
        related_name='tests',
    )

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_dynamic_slug(self, 'title')
        reg = get_object(self.__class__, pk=self.id)  # type: ignore
        if reg and self.title != reg.title:
            self.slug = generate_dynamic_slug(self, 'title')
        return super().save(*args, **kwargs)


class TestTeam(models.Model):
    test = models.ForeignKey(
        'competitions.Test',
        on_delete=models.CASCADE,
    )
    team = models.ForeignKey(
        'editions.Team',
        on_delete=models.CASCADE,
    )
    score = models.FloatField(
        null=True,
        blank=True,
        default=0,
    )
    # winner = models.BooleanField(
    #     null=True,
    #     blank=True,
    # )
    classification = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return str(self.team.name)
