from factory import SubFactory
from factory.django import DjangoModelFactory, FileField
from factory.faker import faker

from home.tests.factories import CollectionFactory

fake = faker.Faker('pt_BR')


class CollectionDocumentsFactory(CollectionFactory):
    collection_type = 'document'


class DocumentFactory(DjangoModelFactory):
    class Meta:
        model = 'documents.Document'
        skip_postgeneration_save = True

    collection = SubFactory(CollectionDocumentsFactory)
    name = fake.pystr(max_chars=100)
    content = FileField(
        data=fake.binary(length=1500),
        filename='document.pdf',
    )
