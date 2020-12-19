from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    division_id = db.Column(db.Integer, db.ForeignKey('division.id'), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False, default='Пользователь')
    items = db.relationship('Item', backref='item_u', lazy='dynamic')

    def __repr__(self):
        return self.login


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    iscompleted = db.Column(db.Boolean, default=False)
    division_id = db.Column(db.Integer, db.ForeignKey('division.id'), nullable=False)
    creation_date = db.Column(db.DateTime)
    completion_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    executor = db.Column(db.String(100))

    def __repr__(self):
        return self.title


class Division(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    users = db.relationship('User', backref='user', lazy='dynamic')
    items = db.relationship('Item', backref='item', lazy='dynamic')

    def __repr__(self):
        return self.name
