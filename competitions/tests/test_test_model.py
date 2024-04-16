from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from pytest import raises as assert_raises

from competitions.models import Test, TestTeam
from editions.models import Team


def test_test_model_title_has_max_length_50(db, test_fixture):  # Review it later
    reg = test_fixture(title='a' * 51)
    with assert_raises(ValidationError):
        reg.full_clean()


def test_test_model_title_is_unique(db, test_fixture):
    with assert_raises(IntegrityError):
        reg1 = test_fixture(title='teste titulo')
        reg2 = test_fixture(title='teste titulo')


def test_test_model_description_default_value_is_blank(db, test_fixture):
    reg = test_fixture()
    description_default = reg._meta.get_field('description').get_default()
    assert description_default == ''


def test_test_model_date_time_default_value_is_none(db, test_fixture):
    reg = test_fixture()
    date_time_default = reg._meta.get_field('date_time').get_default()
    assert date_time_default is None


def test_test_model_teams_has_related_name_tests(db, test_fixture):
    test_reg = test_fixture()
    team_reg = Team.objects.first()
    assert isinstance(team_reg.tests.first(), Test)


def test_test_model_dunder_str_method_returns_test_title(db, test_fixture):
    reg = test_fixture()
    assert str(reg) == reg.title
