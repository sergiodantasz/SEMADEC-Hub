from social_core.backends.oauth import BaseOAuth2

from editions.models import Course
from helpers.user import format_photo_url
from users.models import Email, User


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
        full_name = response.get('nome_registro')
        if social_name := response.get('nome_social'):
            full_name = social_name
        first_name, *_, last_name = full_name.split()
        course = Course.objects.filter(name=response.get('course')).first()
        photo_url = format_photo_url(response.get('foto'))
        user_data = {
            'registration': response.get('identificacao'),
            'full_name': full_name,
            'first_name': first_name,
            'last_name': last_name,
            'cpf': response.get('cpf'),
            'campus': response.get('campus'),
            'course': course,
            'sex': response.get('sexo'),
            'link_type': response.get('tipo_usuario'),
            'date_of_birth': response.get('data_de_nascimento'),
            'photo_url': photo_url,
        }
        if not User.objects.filter(registration=response.get('identificacao')).exists():
            user = User.objects.create(**user_data)
            if personal_email := response.get('email_secundario'):
                Email.objects.create(
                    address=personal_email, email_type='Personal', user=user
                )
            if academic_email := response.get('email_academico'):
                Email.objects.create(
                    address=academic_email, email_type='Academic', user=user
                )
            if school_email := response.get('email_google_classroom'):
                Email.objects.create(
                    address=school_email, email_type='School', user=user
                )
        return {
            'username': response.get('identificacao'),
            'first_name': first_name,
            'last_name': last_name,
            'email': response.get('email_preferencial'),
        }
