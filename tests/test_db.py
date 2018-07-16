from auth.models import User
from main.models import Samsung


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
