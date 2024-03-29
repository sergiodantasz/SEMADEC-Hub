from factory import Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory, FileField, ImageField
from factory.faker import faker
from factory.fuzzy import FuzzyChoice

from archive.models import Collection
from users.tests.factories import UserFactory
from utils.generate_placeholder import generate_placeholder

fake = faker.Faker('pt_BR')


class FileFactory(DjangoModelFactory):
    class Meta:
        model = 'archive.File'
        skip_postgeneration_save = True

    display_name = fake.text(max_nb_chars=225)
    content = Sequence(lambda x: fake.unique.file_path())


class ImageFactory(FileFactory):
    content = ImageField(from_func=generate_placeholder)


class DocumentFactory(FileFactory):
    content = FileField(
        data=fake.binary(length=1500),
        filename='document.pdf',
    )


class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = 'archive.Collection'
        skip_postgeneration_save = True

    administrator = SubFactory(UserFactory)  # Add later
    title = Sequence(lambda x: fake.unique.text(max_nb_chars=200))
    collection_type = FuzzyChoice(Collection.COLLECTION_TYPE_CHOICES)
    slug = Sequence(lambda x: fake.unique.slug())

    @post_generation
    def files(self, created, extracted):
        if not created or not extracted:
            return
        self.files.add(*extracted)

    @post_generation
    def tags(self, created, extracted):
        if not created or not extracted:
            return
        self.tags.add(*extracted)


class CollectionArchiveFactory(CollectionFactory):
    collection_type = 'image'
    cover = ImageField(from_func=generate_placeholder)


class CollectionDocumentsFactory(CollectionFactory):
    collection_type = 'document'
