from django.contrib.auth.models import AbstractUser
from django.db import models


class Campus(models.Model):
    acronym = models.CharField(
        primary_key=True,
        max_length=4,
    )
    name = models.CharField(
        unique=True,
        max_length=50,
    )

    def __str__(self):
        return str(self.name)


class User(AbstractUser):
    registration = models.CharField(
        primary_key=True,
        max_length=14,
    )
    campus = models.ForeignKey(
        'users.Campus',
        on_delete=models.SET_NULL,
        null=True,
        db_column='campus_acronym',
    )
    course = models.ForeignKey(
        'editions.Course',
        on_delete=models.SET_NULL,
        null=True,
        db_column='course_id',
        default=None,
    )
    full_name = models.CharField(
        max_length=200,
    )
    first_name = models.CharField(
        max_length=50,
    )
    last_name = models.CharField(
        max_length=50,
    )
    cpf = models.CharField(
        unique=True,
        max_length=14,
    )
    link_type = models.CharField(
        max_length=20,
    )
    sex = models.CharField(
        max_length=1,
    )
    date_of_birth = models.DateField()
    photo = models.ImageField(
        upload_to='users',
    )

    def __str__(self):
        return str(self.full_name)


class Administrator(models.Model):
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        db_column='user_registration',
    )

    def __str__(self):
        return str(self.user.full_name)


class Email(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        db_column='user_registration',
        related_name='emails',
    )
    address = models.EmailField(
        unique=True,
    )
    email_type = models.CharField(
        max_length=15,
        db_column='type',
    )

    def __str__(self):
        return str(self.address)
