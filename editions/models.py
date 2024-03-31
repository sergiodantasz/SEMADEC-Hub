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
        null=True,
        blank=True,
    )
    teams = models.ManyToManyField(
        to='editions.Team',
        through='editions.EditionTeam',
        related_name='editions',
    )

    @property
    def get_teams(self):
        return self.teams.all()

    @property
    def get_edition_team(self):
        return self.edition_team.all()

    @property
    def get_edition_team_current(self):
        return self.edition_team.all().filter(edition__year=self.year)

    def __str__(self):
        return str(self.name)


class Team(models.Model):
    name = models.CharField(
        max_length=75,
    )

    @property
    def get_editions(self):
        return self.editions.all()

    @property
    def get_edition_team(self):
        return self.edition_team.all()

    def __str__(self):
        return str(self.name)


class EditionTeam(models.Model):
    edition = models.ForeignKey(
        'editions.Edition',
        related_name='edition_team',
        on_delete=models.CASCADE,
        db_column='edition_year',
    )
    team = models.ForeignKey(
        'editions.Team',
        related_name='edition_team',
        on_delete=models.CASCADE,
        db_column='team_id',
    )
    score = models.FloatField(
        null=True,
        blank=True,
        default=0,
    )
    classification = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return f'{self.team} - {self.edition}'


class Class(models.Model):
    course = models.ForeignKey(
        'editions.Course',
        on_delete=models.SET_NULL,
        null=True,
        db_column='course_id',
    )
    team = models.ForeignKey(
        'editions.Team',
        related_name='classes',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return str(self.course.name)
