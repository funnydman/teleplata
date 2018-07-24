from datetime import datetime

from . import db
from .common import MODEL_FIELDS


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


class Brand(db.Model):
    __abstract__ = True
    __searchable__ = MODEL_FIELDS
    id = db.Column(db.Integer, primary_key=True, unique=True)
    model = db.Column(db.String(256), unique=True, nullable=False)
    power = db.Column(db.String(256))
    t_con = db.Column(db.String(256))
    main = db.Column(db.String(256))
    x_main = db.Column(db.String(256))
    y_main = db.Column(db.String(256))
    logic = db.Column(db.String(256))
    invertor = db.Column(db.String(256))
    led_driver = db.Column(db.String(256))
    y_scan = db.Column(db.String(256))
    y_sus = db.Column(db.String(256))

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
