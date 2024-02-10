from factory import Sequence, post_generation
from factory.django import DjangoModelFactory
from factory.faker import faker

fake = faker.Faker('pt_BR')


class TagFactory(DjangoModelFactory):
    class Meta:
        model = 'home.Tag'
        # django_get_or_create = ['name', 'slug']

    name = Sequence(lambda x: fake.unique.pystr(max_chars=50))
    slug = Sequence(lambda x: fake.unique.slug())

    @post_generation
    def clear_unique(self, *args):
        fake.unique.clear()
