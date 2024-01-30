from factory import SubFactory
from factory.django import DjangoModelFactory, ImageField


class AdministratorFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Administrator'

    user = SubFactory('users.User')


class CampusFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Campus'

    acronym = 'cn'
    name = 'Currais Novos'


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
