from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

class User(db.Model, UserMixin):
    # Primary key for user
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    admin = db.Column(db.Boolean, default=False)

class Tickets(db.Model):
    #Primary key for tickets
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    
    title = db.Column(db.String(256), nullable=False)
    severity = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    assigned_group = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime(timezone=True))