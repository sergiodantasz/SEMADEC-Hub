from factory import Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory, ImageField
from factory.faker import faker

from users.tests.factories import AdministratorFactory

fake = faker.Faker('pt_BR')


class NewsFactory(DjangoModelFactory):
    class Meta:
        model = 'news.News'
        skip_postgeneration_save = True

    administrator = SubFactory(AdministratorFactory)
    title = fake.text(max_nb_chars=200)
    excerpt = fake.text(max_nb_chars=200)
    content = fake.text()
    slug = Sequence(lambda x: fake.unique.slug())

    post_generation(fake.unique.clear())
