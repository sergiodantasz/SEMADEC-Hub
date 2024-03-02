from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from authlib.integrations.django_client import OAuth
from django.core.files.images import ImageFile
from django.http import HttpRequest
from dotenv import load_dotenv
from environ import Env
from requests_oauthlib import OAuth2Session

from core.settings import SOCIAL_AUTH_SUAP_KEY, SOCIAL_AUTH_SUAP_SECRET
from editions.models import Course
from helpers.user import create_emails, download_photo
from users.models import Campus, User

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env', override=True)

env = Env()


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


def get_or_create_user_model_registry(
    user_api: UserData, user_emails: dict | tuple
) -> User:
    """Receive an API object and creates a database registry based on its content or simply returns the registry if it already exists.

    Args:
        user_api (UserData): data object retrieved from the API backend.
        user_emails (dict | tuple): collection containing all user e-mails.
    """
    user_query = User.objects.filter(registration=user_api.registration).first()
    if user_query:
        return user_query
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


class SuapOAuth2:
    oauth = OAuth()
    oauth.register(
        name='suap',
        client_id=env.str('SOCIAL_AUTH_SUAP_KEY'),
        client_secret=env.str('SOCIAL_AUTH_SUAP_SECRET'),
        access_token_url='https://suap.ifrn.edu.br/o/token/',
        access_token_params=None,
        authorize_url='https://suap.ifrn.edu.br/o/authorize/',
        authorize_params=None,
        api_base_url='https://suap.ifrn.edu.br/api/',
        client_kwargs={
            'scope': 'identificacao email documentos_pessoais',
        },
    )
    suap = oauth.create_client('suap')

    @classmethod
    def authorize_redirect(cls, request: HttpRequest, redirect_uri: str) -> str:
        return cls.suap.authorize_redirect(request, redirect_uri)

    @classmethod
    def authorize_access_token(cls, request: HttpRequest) -> dict:
        return cls.oauth.suap.authorize_access_token(request)

    @classmethod
    def get_user_data(cls, token: dict) -> dict:
        response = cls.oauth.suap.get('eu', token=token).json()
        response['curso'] = (
            cls.oauth.suap.get(
                'v2/minhas-informacoes/meus-dados/?format=json', token=token
            )
            .json()
            .get('vinculo')
            .get('curso')
        )
        return response
