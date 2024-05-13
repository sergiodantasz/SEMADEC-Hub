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


class Edition(models.Model):
    EDITION_TYPE_CHOICES = (
        ('classes', 'Confronto entre turmas'),
        ('courses', 'Confronto entre cursos'),
    )
    year = models.PositiveSmallIntegerField(
        primary_key=True,
    )
    name = models.CharField(
        unique=True,
        max_length=20,
    )
    edition_type = models.CharField(
        max_length=30,
        choices=EDITION_TYPE_CHOICES,
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
    sports = models.ManyToManyField(
        to='competitions.Sport',
        # through='competitions.SportCategory',  # Is this through field necessary?
        related_name='editions',
    )

    # Add EditionSportCategory?
    @property
    def get_teams(self):
        return self.teams.all()

    @property
    def get_matches(self):
        return self.matches.all()

    @property
    def get_edition_team(self):
        return self.edition_team.all()

    @property
    def get_edition_team_current(self):
        return (
            self.edition_team.all().filter(edition__year=self.year).order_by('-score')
        )

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
        to='editions.Class',
        related_name='teams',
    )

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

    def __str__(self):
        return f'{self.team} - {self.edition}'


class Class(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
    )
    slug = models.SlugField(
        max_length=45,
        unique=True,
    )
    course = models.ForeignKey(
        'editions.Course',
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
