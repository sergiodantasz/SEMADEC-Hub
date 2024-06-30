import pytest

from apps.users.tests.factories import UserFactory
from suap.backends import SuapOAuth2, UserData


@pytest.fixture
def user_data_fixture():
    data = {
        'identificacao': '281718921',
        'nome_registro': 'nome',
        'cpf': 'cpf',
        'email_secundario': 'email1@gmail.com',
        'email_google_classroom': 'email2@gmail.com',
        'email_academico': 'email3@gmail.com',
        'tipo_usuario': 'tipo',
        'sexo': 'sexo',
        'data_de_nascimento': 'data',
        'foto': 'foto.png',
    }
    return data


def test_userdata_class_set_user_permissions_update_reg_permissions(
    db, user_data_fixture
):
    data = user_data_fixture
    UserFactory(
        registration=data.get('identificacao'),
        is_admin=True,
        is_staff=True,
        is_superuser=True,
    )
    user_data = UserData(data)
    assert all(
        (
            user_data.is_admin is True,
            user_data.is_staff is True,
            user_data.is_superuser is True,
        )
    )


def test_suapoauth2_get_user_details_returns_dict(db, user_data_fixture):
    obj = SuapOAuth2()
    data = user_data_fixture
    response = obj.get_user_details(data)
    assert isinstance(response, dict)
