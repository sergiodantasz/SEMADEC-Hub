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
    def news(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.news.add(*extracted)

    @post_generation
    def collection(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.collection.add(*extracted)

    @post_generation
    def document(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.document.add(*extracted)

    @post_generation
    def clear_unique(self, *args):
        fake.unique.clear()
