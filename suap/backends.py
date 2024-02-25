import os
from dataclasses import asdict, dataclass
from io import BytesIO
from pathlib import Path

from django.core.files.images import ImageFile
from requests import get
from social_core.backends.oauth import BaseOAuth2

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
        self.campus = Campus.objects.filter(acronym=response.get('campus')).first()
        self.course = Course.objects.filter(name=response.get('course')).first()
        self.full_name = response.get('nome_social') or response.get('nome_registro')
        self.first_name, *_, self.last_name = self.full_name.split()
        self.cpf = response.get('cpf')
        self.link_type = response.get('tipo_usuario')
        self.sex = response.get('sexo')
        self.date_of_birth = response.get('data_de_nascimento')
        self.photo = download_photo(response.get('foto'), self.registration)


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
        user_api = UserData(response)
        user_reg = User.objects.filter(registration=user_api.registration).first()
        if not user_reg:
            user = User.objects.create(**asdict(user_api))
            create_emails(
                user,
                response.get('email_secundario'),
                response.get('email_google_classroom'),
                response.get('email_academico'),
            )
        else:
            update_fields = []
            for k, v in user_api.__dict__.items():
                if k == 'photo':
                    validation = (
                        getattr(user_reg, k).read() != getattr(user_api, k).read()
                    )
                else:
                    validation = getattr(user_reg, k) != getattr(user_api, k)
                if validation:
                    if k == 'photo':
                        os.remove(Path(user_reg.photo.path))
                    setattr(user_reg, k, v)
                    update_fields.append(k)
            user_reg.save(update_fields=update_fields)
        return {
            'username': user_api.registration,
            'first_name': user_api.first_name,
            'last_name': user_api.last_name,
            'email': response.get('email_preferencial'),
        }
