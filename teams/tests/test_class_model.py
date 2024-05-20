def test_class_model_course_db_column_is_course_id(db, class_fixture):
    reg = class_fixture()
    assert hasattr(reg, 'course_id')


def test_class_model_course_can_be_null(db, class_fixture):
    reg = class_fixture(course=None)
    assert reg.course is None


def test_class_model_dunder_str_method_returns_class_course_name(db, class_fixture):
    reg = class_fixture()
    assert str(reg) == reg.name
