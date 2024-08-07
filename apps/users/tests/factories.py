from factory import LazyAttribute, Sequence, SubFactory
from factory.django import DjangoModelFactory, DjangoOptions, ImageField
from factory.faker import faker

from apps.teams.tests.factories import CourseFactory

fake = faker.Faker('pt_BR')


class CampusFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Campus'
        skip_postgeneration_save = True

    acronym = Sequence(lambda x: fake.unique.pystr(min_chars=2, max_chars=2))
    name = Sequence(lambda x: fake.unique.city())


class UserFactory(DjangoModelFactory, DjangoOptions):
    class Meta:
        model = 'users.User'
        skip_postgeneration_save = True

    registration = Sequence(lambda x: fake.unique.pystr(min_chars=14, max_chars=14))
    campus = SubFactory(CampusFactory)
    course = SubFactory(CourseFactory)
    full_name = fake.name()
    personal_email = Sequence(lambda x: fake.unique.email())
    school_email = Sequence(lambda x: fake.unique.email())
    academic_email = Sequence(lambda x: fake.unique.email())
    cpf = Sequence(lambda x: fake.unique.cpf())
    link_type = fake.pystr(max_chars=20)
    sex = fake.pystr(min_chars=1, max_chars=1)
    date_of_birth = fake.date()
    photo = ImageField()
    password = fake.password(length=15)
