from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
db=SQLAlchemy()

class User(db.Model):
    __tablename__='users'

    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50), unique=True)
    email=db.Column(db.String(50), unique=True)
    password=db.Column(db.String(66))
    create_date=db.Column(db.DateTime, default=datetime.datetime.now)
    comments=db.relationship('Comment')

    def __init__(self,username,password,email):
        self.username=username
        self.password=self.__create_password(password)
        self.email=email

    def __create_password(self, password):
        return generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.password, password)

class Comment(db.Model):
    __tablename='comments'
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    text=db.Column(db.Text())
    create_date=db.Column(db.DateTime, default=datetime.datetime.now)

