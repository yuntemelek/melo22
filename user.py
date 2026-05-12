from datetime import datetime
from extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=True)
    level = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    progress = db.relationship('UserProgress', back_populates='user', cascade='all, delete-orphan')
    memories = db.relationship('MemoryEntry', back_populates='user', cascade='all, delete-orphan')
    chat_sessions = db.relationship('ChatSession', back_populates='user', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'level': self.level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
