from factory.django import DjangoModelFactory
from factory.faker import faker

fake = faker.Faker('pt_BR')


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Course'

    name = fake.catch_phrase()
