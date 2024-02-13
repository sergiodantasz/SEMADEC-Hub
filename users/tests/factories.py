from factory import Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory, DjangoOptions, ImageField
from factory.faker import faker

from editions.tests.factories import CourseFactory

fake = faker.Faker('pt_BR')


class CampusFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Campus'

    # acronym = fake.pystr(min_chars=2, max_chars=2)
    # acronym = fake.unique.pystr(min_chars=2, max_chars=2)
    acronym = Sequence(lambda x: fake.unique.pystr(min_chars=2, max_chars=2))
    name = Sequence(lambda x: fake.unique.city())


class UserFactory(DjangoModelFactory, DjangoOptions):
    class Meta:
        model = 'users.User'
        # skip_postgeneration_save = True

    registration = Sequence(lambda x: fake.unique.pystr(min_chars=14, max_chars=14))
    campus = SubFactory(CampusFactory)
    course = SubFactory(CourseFactory)
    full_name = fake.name()
    first_name = fake.first_name()
    last_name = fake.last_name()
    cpf = Sequence(lambda x: fake.unique.cpf())
    link_type = fake.pystr(max_chars=20)
    sex = fake.pystr(min_chars=1, max_chars=1)
    date_of_birth = fake.date()
    photo = ImageField()

    post_generation(fake.unique.clear())


class AdministratorFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Administrator'
        # django_get_or_create = ['user']

    user = SubFactory(UserFactory)

    # post_generation(fake.unique.clear())


class EmailFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Email'

    user = SubFactory(UserFactory)
    address = Sequence(lambda x: fake.unique.email())
    email_type = fake.pystr(max_chars=15)

    # post_generation(fake.unique.clear())
