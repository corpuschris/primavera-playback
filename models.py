from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    experiences = db.relationship('Experience', backref='user', lazy=True)

class Performance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(100), nullable=False)
    stage = db.Column(db.String(100))
    day = db.Column(db.String(20))  # e.g., "Friday"
    year = db.Column(db.Integer, nullable=False)

    experiences = db.relationship('Experience', backref='performance', lazy=True)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    performance_id = db.Column(db.Integer, db.ForeignKey('performance.id'), nullable=False)
    viewing_status = db.Column(db.String(10))  # watched, glanced, skipped
    rating = db.Column(db.String(10))  # good, okay, bad (only if watched)
