from django.db import models

from editions.models import Course


class Campus(models.Model):
    acronym = models.CharField(
        primary_key=True,
        max_length=4,
    )
    name = models.CharField(
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )


class User(models.Model):
    registration = models.CharField(
        primary_key=True,
        max_length=14,
    )
    campus = models.ForeignKey(
        Campus,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        db_column='campus_acronym',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        db_column='course_id',
        default=None,
    )
    full_name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )
    first_name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    last_name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    cpf = models.CharField(
        unique=True,
        max_length=14,
        null=False,
        blank=False,
    )
    link_type = models.CharField(
        max_length=20,
        null=False,
        blank=False,
    )
    sex = models.CharField(
        max_length=1,
        null=False,
        blank=False,
    )
    date_of_birth = models.DateField(
        null=False,
        blank=False,
    )
    photo_url = models.URLField(
        unique=True,
        null=False,
        blank=False,
    )


class Administrator(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        unique=True,
        null=False,
        blank=False,
        db_column='user_registration',
    )


class Email(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_column='user_registration',
    )
    address = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )
    email_type = models.CharField(
        max_length=15,
        null=False,
        blank=False,
        db_column='type',
    )
