from . import db
from datetime import datetime
from flask_login import UserMixin

# User Model


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-Many relationship: one user -> many goals
    goals = db.relationship('Goal', backref='user',
                            lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User {self.username}>"


# Goal Model
class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    due_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime,  default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Goal {self.title} | Completed: {self.is_completed}>'
