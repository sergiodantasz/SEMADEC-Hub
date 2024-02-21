from email.policy import default

from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=75,
        unique=True,
    )

    def __str__(self):
        return str(self.name)


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
    )
    teams = models.ManyToManyField(
        to='editions.Team',
        through='editions.TeamEdition',
    )

    def __str__(self):
        return str(self.name)


class Class(models.Model):
    course = models.ForeignKey(
        'editions.Course',
        on_delete=models.SET_NULL,
        null=True,
        db_column='course_id',
    )

    def __str__(self):
        return str(self.course.name)


class Team(models.Model):
    name = models.CharField(
        max_length=75,
    )
    classes = models.ManyToManyField(
        to='editions.Class',
    )
    competitions = models.ManyToManyField(
        to='competitions.Competition',
        through='editions.TeamCompetition',
    )
    editions = models.ManyToManyField(
        to='editions.Edition',
        through='editions.TeamEdition',
    )

    def __str__(self):
        return str(self.name)


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
        blank=True,
        default=None,
    )
    classification = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        default=None,
    )
