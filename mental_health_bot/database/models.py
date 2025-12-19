from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    preferences = db.Column(db.String(500), nullable=True) # JSON string for preferences
    consent_given = db.Column(db.Boolean, default=False)
    
    # New Fields for Engagement
    last_checkin_date = db.Column(db.Date, nullable=True)
    streak_count = db.Column(db.Integer, default=0)
    
    chats = db.relationship('ChatHistory', backref='author', lazy='dynamic')
    mood_entries = db.relationship('MoodEntry', backref='user', lazy='dynamic')
    journal_entries = db.relationship('JournalEntry', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_preferences(self):
        if self.preferences:
            return json.loads(self.preferences)
        return {"theme": "dark", "notifications": True}

    def set_preferences(self, preferences):
        self.preferences = json.dumps(preferences)

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'user' or 'bot'
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False) # 1-10
    emotion_tag = db.Column(db.String(50)) # e.g. "Anxious", "Neutral"
    note = db.Column(db.String(256), nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)



class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    url = db.Column(db.String(256))
    category = db.Column(db.String(64)) # e.g. 'anxiety', 'depression'
    sentiment_tag = db.Column(db.String(20)) # 'negative', 'positive'
