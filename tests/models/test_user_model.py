from teleplata.admin.models import User


def test_create_new_user(app, session):
    new_user = User(username=app.config['TEST_USERNAME'], password=app.config['TEST_PASSWORD'])
    session.add(new_user)
    session.commit()
    user_obj = User.query.filter_by(username=app.config['TEST_USERNAME']).first()
    assert user_obj is not None


def test_check_user_password():
    user = User(username="user", password="somepass1")
    assert user.check_password("somepass1")
