from apps.archive.tests.conftest import collection_fixture
from apps.documents.tests.conftest import document_fixture
from apps.users.models import User
from apps.users.tests.conftest import user_fixture
from helpers.model import generate_collection_cover_path, get_object, is_owner


def test_helpers_models_get_object_returns_none_if_object_does_not_exists(db):
    test = get_object(User)
    assert test is None


def test_helpers_models_get_object_returns_object_if_object_exists(db, user_fixture):
    obj = user_fixture()  # Creates registry
    test = get_object(User)
    assert test == obj


def test_helpers_models_is_owner_returns_true_if_user_is_admin(
    db, user_fixture, collection_fixture
):
    user = user_fixture()
    archive = collection_fixture(administrator=user)
    assert is_owner(user, archive) is True


def test_helpers_models_is_owner_returns_false_if_user_is_not_admin(
    db, user_fixture, collection_fixture
):
    user = user_fixture()
    archive = collection_fixture()
    assert is_owner(user, archive) is False


def test_helpers_models_generate_collection_cover_path_returns_correct_path_for_collection_instance(
    db, collection_fixture
):
    reg = collection_fixture()
    path = generate_collection_cover_path(reg, 'test')
    assert path == f'collections/{reg.collection_type}/covers/{'test'}'
