from Farm import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, nullable=False,  primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    aadhaar = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    login = db.relationship('Login', backref='login', lazy=True)

    def __repr__(self):
        return f'{self.name} created his account {self.date}'

class Login(db.Model, UserMixin):
    id = db.Column(db.Integer, nullable=False,  primary_key=True)
    email = db.Column(db.String(30), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    datetime = db.Column(db.DateTime(), default=datetime.utcnow)
    bought = db.relationship('Bought', backref='bought', lazy=True)
    final = db.relationship('Final', backref='final', lazy=True)
    feedback = db.relationship('Feedback', backref='feedback1', lazy=True)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(40), nullable=False)
    feedback = db.Column(db.String(120), nullable=False)
    datetime = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('login.user_id'), nullable=True)

class Crops(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    cropname = db.Column(db.String(30),nullable=False)
    cropcost = db.Column(db.Integer,nullable=False)
    soiltype = db.Column(db.String(30),nullable=False)

class Pesticides(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    category = db.Column(db.String(30),nullable=False)
    pesticidecost = db.Column(db.Integer, nullable=False)
    effective = db.Column(db.String(30),nullable=False)

class Fertilizers(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30),nullable=False)
    cost = db.Column(db.Integer, nullable=False)

class Bought(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    thing = db.Column(db.String(30),nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('login.user_id'), nullable=False)

class Final(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    thing = db.Column(db.String(30),nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('login.user_id'), nullable=False)
    datetime = db.Column(db.DateTime(), default=datetime.utcnow)

class update_logs(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30),nullable=False)
    ocost = db.Column(db.Integer, nullable=False)
    ncost = db.Column(db.Integer, nullable=False)