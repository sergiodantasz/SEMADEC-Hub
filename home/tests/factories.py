from factory import PostGeneration, Sequence
from factory.django import DjangoModelFactory
from factory.faker import faker

fake = faker.Faker('pt_BR')


class TagFactory(DjangoModelFactory):
    class Meta:
        model = 'home.Tag'
        skip_postgeneration_save = True

    name = Sequence(lambda x: fake.unique.pystr(max_chars=50))
    slug = Sequence(lambda x: fake.unique.slug())
    news = PostGeneration(lambda obj, create, extracted: obj.news)
    collection = PostGeneration(lambda obj, create, extracted: obj.collection)
