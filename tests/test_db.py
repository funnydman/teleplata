from teleplata.admin.models import User
from teleplata.main.models import Samsung


def test_brand_table_exists_in_db():
    from teleplata.main.common import BRAND_LIST
    from teleplata.main.utils import get_class_by_tablename
    for item in BRAND_LIST:
        assert get_class_by_tablename(item)


def test_model_fields_exist():
    from teleplata.main.common import MODEL_FIELDS
    new_obj = Samsung(model="test1", power="some")
    for item in MODEL_FIELDS:
        assert item in new_obj.__table__.columns.keys()


def test_restore_backup():
    pass


def test_add_new_entry(session):
    new_obj = Samsung(model="test", power="some")
    session.add(new_obj)
    session.commit()
    obj_sam = Samsung.query.filter_by(model="test").first()
    assert obj_sam.power == "some"


def test_add_new_user(app, session):
    new_user = User(username=app.config['TEST_USERNAME'], password=app.config['TEST_PASSWORD'])
    session.add(new_user)
    session.commit()
    user_obj = User.query.filter_by(username=app.config['TEST_USERNAME']).first()
    assert user_obj is not None
