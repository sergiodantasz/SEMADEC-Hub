from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=75,
        unique=True,
    )


class Edition(models.Model):
    year = models.PositiveSmallIntegerField(
        primary_key=True,
    )
    name = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
    )
    edition_type = models.CharField(
        max_length=10,
        db_column='type',
    )
    theme = models.CharField(
        max_length=100,
        blank=True,
        default='',
    )
    teams = models.ManyToManyField(
        to='editions.Team',
        through='editions.TeamEdition',
    )


class Class(models.Model):
    course = models.ForeignKey(
        'editions.Course',
        on_delete=models.SET_NULL,
        null=True,
        db_column='course_id',
    )


class Team(models.Model):
    name = models.CharField(
        max_length=75,
    )
    classes = models.ManyToManyField(
        to='editions.Class',
    )


class TeamEdition(models.Model):
    edition = models.ForeignKey(
        'editions.Edition',
        on_delete=models.CASCADE,
        db_column='edition_year',
    )
    team = models.ForeignKey(
        'editions.Team',
        on_delete=models.CASCADE,
        db_column='team_id',
    )
    score = models.FloatField(
        null=True,
        default=None,
    )
    classification = models.PositiveSmallIntegerField(
        null=True,
        default=None,
    )


class TeamCompetition(models.Model):
    team = models.ForeignKey(
        'editions.Team',
        on_delete=models.CASCADE,
        db_column='team_id',
    )
    competition = models.ForeignKey(
        'competitions.Competition',
        on_delete=models.CASCADE,
        db_column='competition_id',
    )
    winner = models.BooleanField()
