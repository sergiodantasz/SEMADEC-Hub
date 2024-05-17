from django.utils import timezone
from factory import Sequence, SubFactory, post_generation
from factory.django import DjangoModelFactory, ImageField
from factory.faker import faker
from factory.fuzzy import FuzzyChoice

from users.tests.factories import UserFactory
from utils.generate_placeholder import generate_placeholder

fake = faker.Faker('pt_BR')


class TagFactory(DjangoModelFactory):
    class Meta:
        model = 'home.Tag'
        skip_postgeneration_save = True

    name = Sequence(lambda x: fake.unique.pystr(max_chars=50))
    slug = Sequence(lambda x: fake.unique.slug())


class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = 'home.Collection'
        skip_postgeneration_save = True

    administrator = SubFactory(UserFactory)  # Add later
    title = Sequence(lambda x: fake.unique.text(max_nb_chars=200))
    collection_type = FuzzyChoice(('document', 'image'))
    # cover = ImageField(from_func=generate_placeholder)
    slug = Sequence(lambda x: fake.unique.slug())
    created_at = fake.date_time(tzinfo=timezone.get_current_timezone())
    updated_at = fake.date_time(tzinfo=timezone.get_current_timezone())

    @post_generation
    def tags(self, created, extracted):
        if not created or not extracted:
            return
        self.tags.add(*extracted)
