from dataclasses import asdict, dataclass

from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth.models import User as DjangoUser
from django.contrib.sessions.models import Session
from django.core.files.images import ImageFile
from dotenv import load_dotenv
from environ import Env
from requests_oauthlib import OAuth2Session
from social_core.backends.oauth import BaseOAuth2

from core.settings import SOCIAL_AUTH_SUAP_KEY, SOCIAL_AUTH_SUAP_SECRET
from editions.models import Course
from helpers.user import create_emails, download_photo
from users.models import Campus, User


@dataclass(init=False)
class UserData:
    registration: str
    campus: str
    course: str
    full_name: str
    first_name: str
    first_name: str
    last_name: str
    cpf: str
    link_type: str
    sex: str
    date_of_birth: str
    photo: ImageFile

    def __init__(self, response):
        self.registration = response.get('identificacao')
        self.campus = Campus.objects.filter(acronym=response.get('campus')).first()  # type: ignore
        self.course = Course.objects.filter(name=response.get('course')).first()  # type: ignore
        # Validate the course field (the api sometimes returns different values)
        self.full_name = response.get('nome_social') or response.get('nome_registro')
        self.first_name, *_, self.last_name = self.full_name.split()
        self.cpf = response.get('cpf')
        self.link_type = response.get('tipo_usuario')
        self.sex = response.get('sexo')
        self.date_of_birth = response.get('data_de_nascimento')
        self.photo = download_photo(response.get('foto'), self.registration)


def create_user_model_registry(user_api: UserData, user_emails: dict | tuple) -> User:
    """Receive an API object and creates a database registry based on its content.

    Args:
        user_api (UserData): data object retrieved from the API backend.
        user_emails (dict | tuple): collection containing all user e-mails.
    """
    user_reg = User.objects.create(**asdict(user_api))
    create_emails(user_reg, *user_emails)
    return user_reg


def update_user_model_fields(user_api: UserData, user_reg: User) -> None:
    """Receive both the API and database objects and perform update on the outdated db fields.

    Args:
        user_api (UserData): data object retrieved from the API backend.
        user_reg (User): user registry object retrieved from the database.
    """
    update_fields = []
    for k, v in user_api.__dict__.items():
        if k == 'photo':
            validation = getattr(user_reg, k).read() != getattr(user_api, k).read()
            pre_update = lambda: user_reg.photo.delete()  # noqa: E731
        else:
            validation = getattr(user_reg, k) != getattr(user_api, k)
            pre_update = lambda: ...  # noqa: E731
        if validation:
            pre_update()
            setattr(user_reg, k, v)
            update_fields.append(k)
    user_reg.save(update_fields=update_fields)


# class SuapOAuth2(BaseOAuth2):
#     name = 'suap'
#     AUTHORIZATION_URL = 'https://suap.ifrn.edu.br/o/authorize/'
#     ACCESS_TOKEN_URL = 'https://suap.ifrn.edu.br/o/token/'
#     ACCESS_TOKEN_METHOD = 'POST'
#     ID_KEY = 'identificacao'
#     RESPONSE_TYPE = 'code'
#     REDIRECT_STATE = True
#     STATE_PARAMETER = True
#     USER_DATA_URL = 'https://suap.ifrn.edu.br/api/eu/'
#     EXTRA_USER_DATA_URL = (
#         'https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-dados/'
#     )
#     DEFAULT_SCOPE = ['identificacao', 'email', 'documentos_pessoais']

#     def user_data(self, access_token, *args, **kwargs):
#         method = 'GET'
#         data = {'scope': kwargs.get('response').get('scope')}  # type: ignore
#         headers = {'Authorization': f'Bearer {access_token}'}
#         response = self.request(
#             url=self.USER_DATA_URL, method=method, data=data, headers=headers
#         ).json()
#         extra_response = self.request(
#             url=self.EXTRA_USER_DATA_URL, method=method, headers=headers
#         ).json()
#         course = extra_response.get('vinculo').get('curso')
#         response['curso'] = course
#         return response

#     def get_user_details(self, response):
#         user_api = UserData(response)
#         user_reg = User.objects.filter(registration=user_api.registration).first()
#         if not user_reg:
#             user_emails = (
#                 response.get('email_secundario'),
#                 response.get('email_google_classroom'),
#                 response.get('email_academico'),
#             )
#             user_reg = create_user_model_registry(user_api, user_emails)
#         else:
#             update_user_model_fields(user_api, user_reg)
#         return {
#             'username': user_api.registration,
#             'first_name': user_api.first_name,
#             'last_name': user_api.last_name,
#             'email': response.get('email_preferencial'),
#         }


class SuapOAuth2(BaseBackend):
    client_id = SOCIAL_AUTH_SUAP_KEY
    client_secret = SOCIAL_AUTH_SUAP_SECRET
    redirect_uri = r'http://127.0.0.1:8000/complete/suap/'
    scope = ['identificacao', 'email', 'documentos_pessoais']
    oauth = OAuth2Session(
        client_id,
        redirect_uri=redirect_uri,
        scope=scope,
    )
    authorization_url, scope = oauth.authorization_url(
        'https://suap.ifrn.edu.br/o/authorize/'
    )

    @classmethod
    def fetch_token(cls, suap_uri):
        cls.oauth.fetch_token(
            'https://suap.ifrn.edu.br/o/token/',
            authorization_response=suap_uri,
            client_id=cls.client_id,
            client_secret=cls.client_secret,
            verify=True,
        )
        ...

    @classmethod
    def get(cls, url):
        return cls.oauth.get(url)

    def get_user(self, user_id):
        obj = User.objects.get(registration=user_id)
        ...
        return obj

    def authenticate(self, request, token, username=None):
        obj = User.objects.get(registration=username)
        token_verify = 'token' in request.session
        if obj and not token_verify:
            request.session['token'] = token
            return obj
        return None
