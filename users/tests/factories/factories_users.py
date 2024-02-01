from factory import SubFactory
from factory.django import DjangoModelFactory, DjangoOptions
from factory.faker import faker

from editions.tests.factories.factories_editions import CourseFactory

fake = faker.Faker('pt_BR')


class CampusFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Campus'

    acronym = fake.pystr(min_chars=2, max_chars=2)
    name = fake.city()


class UserFactory(DjangoModelFactory, DjangoOptions):
    class Meta:
        model = 'users.User'
        skip_postgeneration_save = True

    registration = fake.pystr(min_chars=14, max_chars=14)
    campus = SubFactory(CampusFactory)
    course = SubFactory(CourseFactory)
    full_name = fake.name()
    first_name = fake.first_name()
    last_name = fake.last_name()
    cpf = fake.cpf()
    link_type = fake.pystr(max_chars=20)
    sex = fake.pystr(min_chars=1, max_chars=1)
    date_of_birth = fake.date()
    photo_url = fake.image_url(width=1000, height=1000)


class AdministratorFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Administrator'

    user = SubFactory(UserFactory)
