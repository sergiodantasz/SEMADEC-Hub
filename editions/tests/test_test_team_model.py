from django.db import IntegrityError
from pytest import mark
from pytest import raises as assert_raises


@mark.skip
def test_test_team_model_score_cannot_be_negative(db, test_team_fixture):
    with assert_raises(IntegrityError):
        reg = test_team_fixture(score=-10)
