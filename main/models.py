from main import db


class Brand(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, unique=True)
    model = db.Column(db.String(120), unique=True, nullable=False)
    power = db.Column(db.String(120))
    t_con = db.Column(db.String(120))
    x_main = db.Column(db.String(120))
    y_main = db.Column(db.String(120))
    logic = db.Column(db.String(120))
    invertor = db.Column(db.String(120))
    y_scan = db.Column(db.String(120))


class Samsung(Brand):
    __tablename__ = 'samsung'

    def __repr__(self):
        return '<Samsung %r>' % self.model


class Lg(Brand):
    __tablename__ = 'lg'

    def __repr__(self):
        return '<Lg %r>' % self.model
