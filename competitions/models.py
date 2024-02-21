from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=15,
        unique=True,
    )

    def __str__(self):
        return str(self.name)


class Sport(models.Model):
    name = models.CharField(
        max_length=30,
    )
    category = models.ForeignKey(
        'competitions.Category',
        on_delete=models.CASCADE,
        db_column='category_id',
    )
    date_time = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return str(self.name)


class Test(models.Model):
    title = models.CharField(
        max_length=50,
        unique=True,  # I think it should have unique constraint
    )
    description = models.TextField(
        blank=True,
        default='',
    )
    date_time = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return str(self.title)


class TestOrSport(models.Model):
    test = models.OneToOneField(
        'competitions.Test',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        db_column='test_id',
    )
    sport = models.OneToOneField(
        'competitions.Sport',
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        db_column='sport_id',
    )


class Competition(models.Model):
    edition = models.ForeignKey(
        'editions.Edition',
        on_delete=models.CASCADE,
        db_column='year_edition',
    )
    test_or_sport = models.ForeignKey(
        'competitions.TestOrSport',
        on_delete=models.CASCADE,
        db_column='test_or_sport_id',
    )

    def __str__(self):
        return str(self.edition.name)
