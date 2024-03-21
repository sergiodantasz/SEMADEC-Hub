from django.contrib.auth.models import AbstractUser as DjangoAbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
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


class UserManager(DjangoUserManager):
    def create_user(
        self,
        registration,
        campus,
        course,
        full_name,
        personal_email,
        school_email,
        academic_email,
        cpf,
        link_type,
        sex,
        date_of_birth,
        photo,
        is_admin,
    ):
        user = self.model(
            registration=registration,
            campus=campus,
            course=course,
            full_name=full_name,
            personal_email=personal_email,
            school_email=school_email,
            academic_email=academic_email,
            cpf=cpf,
            link_type=link_type,
            sex=sex,
            date_of_birth=date_of_birth,
            photo=photo,
            is_admin=is_admin,
        )
        user.set_password(self.make_random_password(100))
        user.save(using=self._db)
        return user

    # TODO: override create_superuser method


class User(DjangoAbstractUser):
    registration = models.CharField(
        primary_key=True,
        max_length=14,
    )
    campus = models.ForeignKey(
        'users.Campus',
        on_delete=models.SET_NULL,
        null=True,
        db_column='campus_acronym',
        default=None,
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
    personal_email = models.EmailField(
        unique=True,
        max_length=250,
    )
    school_email = models.EmailField(
        unique=True,
        max_length=250,
    )
    academic_email = models.EmailField(
        unique=True,
        max_length=250,
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
    is_admin = models.BooleanField(
        default=False,
    )

    objects = UserManager()
    email = None
    username = None
    USERNAME_FIELD = 'registration'
    REQUIRED_FIELDS = [
        'full_name',
        'personal_email',
        'school_email',
        'academic_email',
        'cpf',
        'link_type',
        'sex',
        'date_of_birth',
        'photo',
        'is_admin',
    ]

    def __str__(self):
        return f'{self.full_name} ({self.registration})'

    def first_name(self):
        return self.full_name.split()[0]

    def last_name(self):
        return self.full_name.split()[-1]
