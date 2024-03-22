from factory import PostGeneration, Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory, FileField, ImageField
from factory.faker import faker
from factory.fuzzy import FuzzyChoice

from archive.models import Collection
from home.tests.factories import TagFactory
from users.tests.factories import UserFactory
from utils.generate_placeholder import generate_placeholder

fake = faker.Faker('pt_BR')


class FileFactory(DjangoModelFactory):
    class Meta:
        model = 'archive.File'
        skip_postgeneration_save = True

    display_name = fake.text(max_nb_chars=225)
    content = Sequence(lambda x: fake.unique.file_path())

    # post_generation(fake.unique.clear())


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
    files = PostGeneration(lambda obj, create, extracted: obj.files)
    title = Sequence(lambda x: fake.unique.text(max_nb_chars=200))
    collection_type = FuzzyChoice(Collection.COLLECTION_TYPE_CHOICES)
    slug = Sequence(lambda x: fake.unique.slug())
    tags = PostGeneration(lambda obj, create, extracted: obj.tags)
    post_generation(fake.unique.clear())


class CollectionArchiveFactory(CollectionFactory):
    collection_type = 'image'
    cover = ImageField(from_func=generate_placeholder)

    @post_generation
    def files(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.files.add(*extracted)


class CollectionDocumentsFactory(CollectionFactory):
    collection_type = 'document'

    @post_generation
    def files(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.files.add(*extracted)
