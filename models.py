from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60))
