from flask import Flask, redirect, url_for, render_template, request
from flask_admin import Admin
from flask_admin.base import AdminIndexView
from flask_login.utils import login_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import backref
import os
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from flask_admin.menu import MenuLink  # logout


path = os.getcwd()
parent = os.path.dirname(path)
filename = os.path.join(parent, "test1\mydb.db")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + filename
app.config["SECRET_KEY"] = "123abc"
app.config["SERVER_NAME"] = "127.0.0.1:5000"

db = SQLAlchemy(app)
login = LoginManager(app)


@login.user_loader
def load_user(user_id):
    return UserAdmin.query.get(user_id)


class UserAdmin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255))


class Authors(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    birthday = db.Column(db.DateTime, nullable=False)
    books = db.relationship(
        "Books", cascade="all,delete", backref="author", lazy="dynamic"
    )

    def __repr__(self):
        return self.name


class Books(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))
    pub_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return self.title


@app.route("/login", methods=["POST", "GET"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = UserAdmin.query.filter_by(email=email).first()

    if not user or not user.password==password:
        return render_template("login.html")

    user = UserAdmin.query.get(1)
    login_user(user)

    return redirect("/admin/")


@app.route("/logout")
def logout():
    logout_user()
    return "You have been Logged out"


class MyModelView(ModelView):  # для закриття окремих моделей
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))


class MyAdminIndexView(AdminIndexView):  # для закриття всієї адмінки
    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app, index_view=MyAdminIndexView())
with app.app_context():
    admin.add_link(MenuLink(name="Logout", category="", url=url_for("logout")))


admin.add_view(MyModelView(Authors, db.session))
admin.add_view(MyModelView(Books, db.session))
admin.add_view(MyModelView(UserAdmin, db.session))


if __name__ == "__main__":
    app.run(debug=True)
