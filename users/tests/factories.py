from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory, DjangoOptions
from factory.faker import faker

from editions.tests.factories import CourseFactory

fake = faker.Faker('pt_BR')


class CampusFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Campus'

    # acronym = fake.pystr(min_chars=2, max_chars=2)
    # acronym = fake.unique.pystr(min_chars=2, max_chars=2)
    acronym = Sequence(lambda x: fake.unique.pystr(min_chars=2, max_chars=2))
    name = Sequence(lambda x: fake.city())


class UserFactory(DjangoModelFactory, DjangoOptions):
    class Meta:
        model = 'users.User'
        # django_get_or_create = ['photo_url', 'registration']
        # skip_postgeneration_save = True

    registration = Sequence(lambda x: fake.pystr(min_chars=14, max_chars=14))
    campus = SubFactory(CampusFactory)
    course = SubFactory(CourseFactory)
    full_name = fake.name()
    first_name = fake.first_name()
    last_name = fake.last_name()
    cpf = Sequence(lambda x: fake.cpf())
    link_type = fake.pystr(max_chars=20)
    sex = fake.pystr(min_chars=1, max_chars=1)
    date_of_birth = fake.date()
    # photo_url = Sequence(lambda x: fake.image_url(width=1000, height=1000))


class AdministratorFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Administrator'
        # django_get_or_create = ['user']

    user = SubFactory(UserFactory)
