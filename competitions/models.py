from django.db import models

from editions.models import Edition


class Sport(models.Model):
    name = models.CharField(
        max_length=30,
        null=False,
        blank=False,
    )
    category = models.CharField(  # Woudn't it be better to create another table?
        max_length=15,
        null=False,
        blank=False,
    )
    date_time = models.DateTimeField(
        null=True,
        blank=False,  # Is it good to allow null but not allow blank?
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
    date_time = models.DateTimeField(
        null=True,
        blank=False,  # Is it good to allow null but not allow blank?
    )


class TestOrSport(models.Model):  # Check it again later
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    sport = models.ForeignKey(
        Sport,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )


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
