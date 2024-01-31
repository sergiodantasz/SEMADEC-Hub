from factory import Faker, SubFactory
from factory.django import DjangoModelFactory


class AdministratorFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Administrator'

    user = SubFactory('users.User')


class CampusFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Campus'

    acronym = Faker('pystr', min_chars=2, max_chars=2)
    name = Faker('city')


class UserFactory(DjangoModelFactory):
    class Meta:
        model = 'users.User'

    registration = '20211034010020'
    campus = SubFactory('users.Campus')
    course = SubFactory('editions.Course')
    full_name = 'Joamerson Islan Santos Amaral'
    first_name = 'Joamerson'
    last_name = 'Amaral'
    cpf = '532.183.190-34'
    link_type = 'aluno'
    sex = 'm'
    date_of_birth = '02/01/2006'
    photo_url = 'https://suap.ifrn.edu.br/photos/photo.jpg'
