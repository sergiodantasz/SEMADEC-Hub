from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=15,
        unique=True,
        null=False,
        blank=False,
    )


class Sport(models.Model):
    name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
    )
    category = models.ForeignKey(
        'competitions.Category',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_column='category_id',
    )
    date_time = models.DateTimeField(
        blank=False,
        default=None,
    )


class Test(models.Model):
    title = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    description = models.TextField(
        null=False,
        blank=True,
        default='',
    )
    date_time = models.DateTimeField(
        blank=False,
        default=None,
    )


class TestOrSport(models.Model):
    test = models.OneToOneField(
        'competitions.Test',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        default=None,
        db_column='test_id',
    )
    sport = models.OneToOneField(
        'competitions.Sport',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        default=None,
        db_column='sport_id',
    )


class Competition(models.Model):
    edition = models.ForeignKey(
        'editions.Edition',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_column='edition_year',
    )
    test_or_sport = models.ForeignKey(
        'competitions.TestOrSport',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_column='test_or_sport_id',
    )
    teams = models.ManyToManyField(
        to='editions.Team',
        through='editions.TeamCompetition',
    )
