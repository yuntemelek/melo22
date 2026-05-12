from datetime import datetime
from extensions import db

class MemoryEntry(db.Model):
    __tablename__ = 'memory_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=True)
    entry_type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='memories')
    topic = db.relationship('Topic')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'topic_id': self.topic_id,
            'entry_type': self.entry_type,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
