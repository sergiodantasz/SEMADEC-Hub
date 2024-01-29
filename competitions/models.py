from django.db import models

from editions.models import Edition


class Competition(models.Model):
    edition = models.ForeignKey(
        Edition,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_column='edition_year',
    )
    test_or_sport = models.ForeignKey(
        TestOrSport,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_column='test_or_sport_id',
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
    )
    date_time = models.DateTimeField(  # Check it again later
        null=True,
        blank=True,
    )


class Sport(models.Model):
    ...


class TestOrSport(models.Model):
    ...
