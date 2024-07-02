from django.db.models import QuerySet
from django.utils.safestring import mark_safe

from apps.archive.tests.factories import ImageFactory
from apps.home.templatetags import custom_tags
from apps.home.tests.factories import TagFactory
from apps.users.models import User
from apps.users.tests.factories import UserFactory


def test_load_regs_returns_str_object(db):
    regs = TagFactory.create_batch(5)
    response = custom_tags.load_regs(
        db_regs=regs,
        template='archive/partials/_archive-item.html',
        empty='Ocorreu um erro',
    )
    assert isinstance(response, str)


def test_load_regs_generate_safe_response(db):
    regs = TagFactory.create_batch(5)
    response = custom_tags.load_regs(
        db_regs=regs,
        template='archive/partials/_archive-item.html',
        empty='Ocorreu um erro',
    )
    assert response == mark_safe(response)


def test_load_regs_returns_nothing_found_tag_if_no_db_regs_provided(db):
    response = custom_tags.load_regs(
        db_regs=[],
        template='archive/partials/_archive-item.html',
        empty='Ocorreu um erro',
    )
    assert 'nothing-found' in response


def test_load_regs_returns_container_if_db_regs_are_provided(db):
    regs = TagFactory.create_batch(5)
    response = custom_tags.load_regs(
        db_regs=regs,
        template='archive/partials/_archive-item.html',
        empty='Ocorreu um erro',
    )
    assert 'nothing-found' not in response


def test_load_regs_returns_container_with_div_if_div_is_provided(db):
    regs = TagFactory.create_batch(5)
    div_name = 'test-div-name'
    response = custom_tags.load_regs(
        db_regs=regs,
        template='archive/partials/_archive-item.html',
        empty='Ocorreu um erro',
        div=div_name,
    )
    assert div_name in response


def test_check_error_returns_empty_str_if_no_errors(db, tag_form_fixture):
    form = tag_form_fixture()
    field = [f for f in form][0]
    response = custom_tags.check_error(field)
    assert response == ''


def test_check_error_returns_str_if_field_has_errors(db, tag_form_fixture):
    form = tag_form_fixture()
    field = [f for f in form][0]
    form.add_error(field.name, 'error test')
    response = custom_tags.check_error(field)
    assert response != ''


def test_check_error_returns_all_errors(db, tag_form_fixture):
    form = tag_form_fixture()
    field = [f for f in form][0]
    form.add_error(field.name, 'error_test1')
    form.add_error(field.name, 'error_test2')
    response = custom_tags.check_error(field)
    assert all(('error_test1' in response, 'error_test2' in response))


def test_load_create_button_returns_dict_with_dispatcher_if_dispatcher_is_not_none(
    db, tag_fixture
):
    user = UserFactory()
    tag = tag_fixture()
    response = custom_tags.load_create_button(
        user=user,
        namespace='home:tags:delete',
        label='test',
        dispatcher=tag.pk,
        id_field='slug',
    )
    assert all(
        (
            isinstance(response['user'], User),
            isinstance(response['namespace'], str),
            str(tag.pk) in response['namespace'],
            isinstance(response['label'], str),
        )
    )


def test_load_create_button_returns_dict_without_dispatcher_if_dispatcher_is_none(
    db, tag_fixture
):
    user = UserFactory()
    tag = tag_fixture()
    response = custom_tags.load_create_button(
        user=user,
        namespace='home:tags:home',
        label='test',
    )
    assert all(
        (
            isinstance(response['user'], User),
            isinstance(response['namespace'], str),
            str(tag.pk) not in response['namespace'],
            isinstance(response['label'], str),
        )
    )


def test_filename_returns_str_object(db):
    file = ImageFactory()
    response = custom_tags.filename(file.content)
    file.content.close()
    assert isinstance(response, str)
