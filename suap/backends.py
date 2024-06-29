from dataclasses import asdict, dataclass

from social_core.backends.oauth import BaseOAuth2

from apps.teams.models import Course
from apps.users.models import Campus, User
from helpers.model import get_object


@dataclass(init=False)
class UserData:
    registration: str
    campus: str
    course: str
    full_name: str
    cpf: str
    personal_email: str
    school_email: str
    academic_email: str
    link_type: str
    sex: str
    date_of_birth: str
    photo: str
    is_admin: bool = False
    is_staff: bool = False
    is_superuser: bool = False

    def __init__(self, response) -> None:
        self.registration = response.get('identificacao')
        self.campus = Campus.objects.filter(acronym=response.get('campus')).first()  # type: ignore
        self.course = Course.objects.filter(name=response.get('course')).first()  # type: ignore
        # Validate the course field (the api sometimes returns different values)
        self.full_name = response.get('nome_social') or response.get('nome_registro')
        self.cpf = response.get('cpf')
        self.personal_email = response.get('email_secundario')
        self.school_email = response.get('email_google_classroom')
        self.academic_email = response.get('email_academico')
        self.link_type = response.get('tipo_usuario')
        self.sex = response.get('sexo')
        self.date_of_birth = response.get('data_de_nascimento')
        self.photo = response.get('foto')
        if user_obj := get_object(User, registration=self.registration):
            self.set_user_permissions(user_obj)

    def set_user_permissions(self, user_obj) -> None:
        self.is_admin = user_obj.is_admin
        self.is_staff = user_obj.is_staff
        self.is_superuser = user_obj.is_superuser


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
        data = {'scope': ' '.join(self.DEFAULT_SCOPE)}
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.request(
            url=self.USER_DATA_URL, method=method, data=data, headers=headers
        ).json()
        extra_response = self.request(
            url=self.EXTRA_USER_DATA_URL, method=method, headers=headers
        ).json()
        photo = extra_response.get('url_foto_150x200')
        course = extra_response.get('vinculo').get('curso')
        response['foto'] = photo
        response['curso'] = course
        return response

    def get_user_details(self, response):
        user_data = UserData(response)
        return asdict(user_data)
