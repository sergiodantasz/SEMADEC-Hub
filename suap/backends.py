from social_core.backends.oauth import BaseOAuth2

from editions.models import Course
from helpers.model import update_model_fields
from helpers.user import create_emails, download_photo
from users.models import Campus, User


class SuapOAuth2(BaseOAuth2):
    name = 'suap'
    AUTHORIZATION_URL = 'https://suap.ifrn.edu.br/o/authorize/'
    ACCESS_TOKEN_URL = 'https://suap.ifrn.edu.br/o/token/'
    ACCESS_TOKEN_METHOD = 'POST'
    ID_KEY = 'identificacao'
    RESPONSE_TYPE = 'code'
    REDIRECT_STATE = True
    STATE_PARAMETER = True
    USER_DATA_URL = 'https://suap.ifrn.edu.br/api/eu/'
    EXTRA_USER_DATA_URL = (
        'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-dados/'
    )
    DEFAULT_SCOPE = ['identificacao', 'email', 'documentos_pessoais']

    def user_data(self, access_token, *args, **kwargs):
        method = 'GET'
        data = {'scope': kwargs.get('response').get('scope')}  # type: ignore
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.request(
            url=self.USER_DATA_URL, method=method, data=data, headers=headers
        ).json()
        extra_response = self.request(
            url=self.EXTRA_USER_DATA_URL, method=method, headers=headers
        ).json()
        course = extra_response.get('vinculo').get('curso')
        response['curso'] = course
        return response

    def get_user_details(self, response):
        registration = response.get('identificacao')
        full_name = response.get('nome_registro')
        if social_name := response.get('nome_social'):
            full_name = social_name
        first_name, *_, last_name = full_name.split()
        campus = Campus.objects.filter(acronym=response.get('campus')).first()
        course = Course.objects.filter(name=response.get('course')).first()
        photo = download_photo(response.get('foto'), registration)
        user_data = {
            'registration': registration,
            'full_name': full_name,
            'first_name': first_name,
            'last_name': last_name,
            'cpf': response.get('cpf'),
            'campus': campus,
            'course': course,
            'sex': response.get('sexo'),
            'link_type': response.get('tipo_usuario'),
            'date_of_birth': response.get('data_de_nascimento'),
            'photo': photo,
        }
        if not User.objects.filter(registration=registration).exists():
            user = User.objects.create(**user_data)
            create_emails(
                user,
                response.get('email_secundario'),
                response.get('email_google_classroom'),
                response.get('email_academico'),
            )
        else:
            user = User.objects.get(registration=registration)
            update_model_fields(user, user_data, ['photo'])
            if not user.photo.storage.exists(user.photo.name):
                setattr(user, 'photo', photo)
                user.save()
            elif photo.read() != user.photo.read():  # Refactor later
                user.photo.delete()
                setattr(user, 'photo', photo)
                user.save()
        return {
            'username': registration,
            'first_name': first_name,
            'last_name': last_name,
            'email': response.get('email_preferencial'),
        }
