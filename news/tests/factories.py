from django.utils import timezone
from factory import Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory
from factory.faker import faker

from users.tests.factories import UserFactory

fake = faker.Faker('pt_BR')


class NewsFactory(DjangoModelFactory):
    class Meta:
        model = 'news.News'
        skip_postgeneration_save = True

    administrator = SubFactory(UserFactory)
    title = fake.text(max_nb_chars=200)
    excerpt = fake.text(max_nb_chars=200)
    content = fake.text(max_nb_chars=10000)
    slug = Sequence(lambda x: fake.unique.slug())
    created_at = fake.date_time(tzinfo=timezone.get_current_timezone())
    updated_at = fake.date_time(tzinfo=timezone.get_current_timezone())

    @post_generation
    def tags(self, create, extracted):
        if not create or not extracted:
            return
        self.tags.add(*extracted)

    @post_generation
    def storage_method(self, create, storage_method):
        if not create or not storage_method:
            return
        self.storage_method = storage_method
