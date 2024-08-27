import pytest
from django.conf import settings

from apps.competitions.tests.factories import (
    MatchTeamFactory,
    SportFactory,
    TestTeamFactory,
    TestWithTeamFactory,
)
from apps.editions.forms import EditionForm, EditionTeamForm
from apps.editions.tests.factories import (
    EditionTeamFactory,
    EditionWith2TeamsFactory,
    TeamWith2EditionsFactory,
)


@pytest.fixture
def edition_fixture():
    sports = SportFactory.create_batch(2)
    edition_factory = EditionWith2TeamsFactory
    edition_factory._meta.django_get_or_create = ''

    caller = lambda **kwargs: edition_factory(  # noqa
        sports=sports, **kwargs
    )
    yield caller


@pytest.fixture
def edition_form_fixture():
    data = {
        'year': 2000,
        'name': 'name',
        'edition_type': 'courses',
        'theme': 'theme',
        'teams': TeamWith2EditionsFactory.create_batch(2),
        'sports': SportFactory.create_batch(3),
    }
    caller = lambda **kwargs: EditionForm(data=data | kwargs)  # noqa
    yield caller


@pytest.fixture
def edition_team_fixture():
    yield EditionTeamFactory


@pytest.fixture
def edition_team_form_fixture():
    data = {
        'score': 10,
    }
    caller = lambda **kwargs: EditionTeamForm(data=data | kwargs)  # noqa
    yield caller


@pytest.fixture
def match_team_fixture():
    yield MatchTeamFactory


def test_fixture():
    yield TestWithTeamFactory


@pytest.fixture
def test_team_fixture():
    yield TestTeamFactory


if __name__.startswith('test'):
    settings.STORAGES['default']['BACKEND'] = (
        'django.core.files.storage.InMemoryStorage'
    )
