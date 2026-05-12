from datetime import datetime
from extensions import db

class Topic(db.Model):
    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    title_tr = db.Column(db.String(160), nullable=False)
    description_tr = db.Column(db.Text, nullable=False)
    level = db.Column(db.String(10), nullable=False)

    progress = db.relationship('UserProgress', back_populates='topic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'title_tr': self.title_tr,
            'description_tr': self.description_tr,
            'level': self.level,
        }

class UserProgress(db.Model):
    __tablename__ = 'user_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    accuracy_rate = db.Column(db.Float, nullable=False, default=0.0)
    attempts = db.Column(db.Integer, nullable=False, default=0)
    last_practiced_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='progress')
    topic = db.relationship('Topic', back_populates='progress')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'topic_id': self.topic_id,
            'accuracy_rate': self.accuracy_rate,
            'attempts': self.attempts,
            'last_practiced_at': self.last_practiced_at.isoformat() if self.last_practiced_at else None,
        }
