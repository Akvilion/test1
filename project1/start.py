import logging
from flask import Flask, redirect, url_for
from flask_admin import Admin
from flask_admin.base import AdminIndexView
from flask_login.utils import login_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import backref
import os
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user


path = os.getcwd()
parent = os.path.dirname(path)
filename = os.path.join(parent, "test1\mydb.db")

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/code/test1/mydb.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+filename
app.config['SECRET_KEY']= '123abc'

db = SQLAlchemy(app)
login = LoginManager(app)


@login.user_loader
def load_user(user_id):
    return UserAdmin.query.get(user_id)





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


class MyModelView(ModelView):  # для закриття окремих моделей
    def is_accessible(self):
        return current_user.is_authenticated


@app.route('/login')
def login():
    user = UserAdmin.query.get(1)
    login_user(user)
    return 'Ligged in'


@app.route('/logout')
def logout():
    logout_user()
    return 'You have been Logged out'


class MyAdminIndexView(AdminIndexView):  # для закриття всієї адмінки
    def is_accessible(self):
        return current_user.is_authenticated
    
    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect(url_for('login'))


admin = Admin(app, index_view=MyAdminIndexView())

admin.add_view(ModelView(Authors, db.session))  # щоб заборонити показувати
admin.add_view(ModelView(Books, db.session))  # MyModelView щоб заборонити показувати
admin.add_view(ModelView(UserAdmin, db.session))


if __name__ == '__main__':
    app.run(debug=True)

