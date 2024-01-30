from factory import SubFactory
from factory.django import DjangoModelFactory, ImageField


class Course(DjangoModelFactory):
    class Meta:
        model = 'editions.Course'

    name = 'Curso Integrado em Informática'
