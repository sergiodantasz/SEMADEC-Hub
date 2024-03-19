from factory import PostGeneration, Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory, FileField, ImageField
from factory.faker import faker
from factory.fuzzy import FuzzyChoice

from archive.models import Collection
from home.tests.factories import TagFactory
from users.tests.factories import AdministratorFactory

fake = faker.Faker('pt_BR')


class FileFactory(DjangoModelFactory):
    class Meta:
        model = 'archive.File'
        skip_postgeneration_save = True

    display_name = fake.text(max_nb_chars=225)
    content = Sequence(lambda x: fake.unique.file_path())

    # post_generation(fake.unique.clear())


class ImageFactory(FileFactory):
    content = ImageField()


class DocumentFactory(FileFactory):
    content = FileField(
        data=fake.binary(length=18927821),
        filename='document.pdf',
    )


class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = 'archive.Collection'
        skip_postgeneration_save = True

    administrator = SubFactory(AdministratorFactory)  # Add later
    files = PostGeneration(lambda obj, create, extracted: obj.files)
    title = Sequence(lambda x: fake.unique.text(max_nb_chars=200))
    type = FuzzyChoice(Collection.COLLECTION_TYPE_CHOICES)
    slug = Sequence(lambda x: fake.unique.slug())
    tags = PostGeneration(lambda obj, create, extracted: obj.tags)
    post_generation(fake.unique.clear())


class CollectionArchiveFactory(CollectionFactory):
    type = 'image'

    @post_generation
    def files(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.files.add(*extracted)


class CollectionDocumentsFactory(CollectionFactory):
    type = 'document'

    @post_generation
    def files(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.files.add(*extracted)
