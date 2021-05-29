from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import backref
import os
from flask_login import UserMixin


path = os.getcwd()
parent = os.path.dirname(path)
filename = os.path.join(parent, "test1\mydb.db")

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/code/test1/mydb.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+filename
app.config['SECRET_KEY']= '123abc'

db = SQLAlchemy(app)

class UserAdmin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    password = db.Column(db.String(255))


class Authors(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    birthday = db.Column(db.DateTime, nullable=False)
    books = db.relationship('Books', cascade="all,delete", backref='author', lazy='dynamic')

    def __repr__(self):
        return self.name


class Books(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    pub_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return self.title


class MyModelView(ModelView):
    pass



admin = Admin(app)

admin.add_view(ModelView(Authors, db.session))
admin.add_view(ModelView(Books, db.session))
admin.add_view(ModelView(UserAdmin, db.session))


if __name__ == '__main__':
    app.run(debug=True)

