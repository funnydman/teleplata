from main.models import Samsung


def test_add_new_entry(session):
    new_obj = Samsung(model="test", power="some")
    session.add(new_obj)
    session.commit()
    obj_sam = Samsung.query.filter_by(model="test").first()
    assert obj_sam.power == "some"
