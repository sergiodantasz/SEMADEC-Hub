from factory import SubFactory
from factory.django import DjangoModelFactory, ImageField


class CourseFactory(DjangoModelFactory):
    class Meta:
        model = 'editions.Course'

    name = 'Curso Integrado em Informática'
