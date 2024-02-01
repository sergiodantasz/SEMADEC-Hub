from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import faker

fake = faker.Faker('pt_BR')


class DocumentFactory(DjangoModelFactory):
    class Meta:
        model = 'documents.Document'
