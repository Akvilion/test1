from .start import db

class Author(db.Model):
    id = db.Column(db.integer, primary_key=True)
    name = db.Colum(db.String(30))
    birthday = db.Colum(db.DateTime, nullable=False)

class Books(db.Model):
    pass