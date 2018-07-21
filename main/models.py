from datetime import datetime

from main import db
from main.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    power_img = db.Column(db.String(200))
    t_con_img = db.Column(db.String(200))
    x_main_img = db.Column(db.String(200))
    y_main_img = db.Column(db.String(200))
    logic_img = db.Column(db.String(200))
    invertor_img = db.Column(db.String(200))
    y_scan_img = db.Column(db.String(200))


class Brand(SearchableMixin, db.Model):
    __abstract__ = True
    __searchable__ = ['model', 'power', 't_con', 'x_main', 'y_main', 'logic', 'invertor', 'y_scan']
    id = db.Column(db.Integer, primary_key=True, unique=True)
    model = db.Column(db.String(120), unique=True, nullable=False)
    power = db.Column(db.String(120))
    t_con = db.Column(db.String(120))
    x_main = db.Column(db.String(120))
    y_main = db.Column(db.String(120))
    logic = db.Column(db.String(120))
    invertor = db.Column(db.String(120))
    y_scan = db.Column(db.String(120))

    pub_date = db.Column(db.DateTime,
                         default=datetime.utcnow)


class Samsung(Brand):
    __tablename__ = 'samsung'
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))

    # define relationship
    image = db.relationship('Image', backref='image')

    def __repr__(self):
        return '<Samsung %r>' % self.model


class Lg(Brand):
    __tablename__ = 'lg'

    def __repr__(self):
        return '<Lg %r>' % self.model


class Horizont(Brand):
    __tablename__ = 'horizont'

    def __repr__(self):
        return '<Horizont %r>' % self.model


class Vityaz(Brand):
    __tablename__ = 'vityaz'

    def __repr__(self):
        return '<Lg %r>' % self.model


class Philips(Brand):
    __tablename__ = 'philips'

    def __repr__(self):
        return '<Philips %r>' % self.model


class Toshiba(Brand):
    __tablename__ = 'toshiba'

    def __repr__(self):
        return '<Toshiba %r>' % self.model


class Tomson(Brand):
    __tablename__ = 'tomson'

    def __repr__(self):
        return '<Tomson %r>' % self.model


class Sharp(Brand):
    __tablename__ = 'sharp'

    def __repr__(self):
        return '<Sharp %r>' % self.model


class Sony(Brand):
    __tablename__ = 'sony'

    def __repr__(self):
        return '<Sony %r>' % self.model


class Panasonic(Brand):
    __tablename__ = 'panasonic'

    def __repr__(self):
        return '<Panasonic %r>' % self.model


class Bbk(Brand):
    __tablename__ = 'bbk'

    def __repr__(self):
        return '<Bbk %r>' % self.model


class Shinco(Brand):
    __tablename__ = 'shinco'

    def __repr__(self):
        return '<Shinco %r>' % self.model


class Dynex(Brand):
    __tablename__ = 'dynex'

    def __repr__(self):
        return '<Dynex %r>' % self.model


class Manta(Brand):
    __tablename__ = 'manta'

    def __repr__(self):
        return '<Manta %r>' % self.model


class Dell(Brand):
    __tablename__ = 'dell'

    def __repr__(self):
        return '<Dell %r>' % self.model


class Daevoo(Brand):
    __tablename__ = 'daevoo'

    def __repr__(self):
        return '<Daevoo %r>' % self.model


class Shivaki(Brand):
    __tablename__ = 'shivaki'

    def __repr__(self):
        return '<Shivaki %r>' % self.model


class Supra(Brand):
    __tablename__ = 'supra'

    def __repr__(self):
        return '<Supra %r>' % self.model


class Grundic(Brand):
    __tablename__ = 'grundic'

    def __repr__(self):
        return '<Grundic %r>' % self.model


class Telefunken(Brand):
    __tablename__ = 'telefunken'

    def __repr__(self):
        return '<Telefunken %r>' % self.model
