from extensions import db
from models.memory import MemoryEntry


def oturum_hafizasi_kaydet(user_id, topic_id, answers, accuracy_rate):
    wrong_answers = [answer for answer in answers if not answer.get('correct')]
    if wrong_answers:
        entry = MemoryEntry(
            user_id=user_id,
            topic_id=topic_id,
            entry_type='wrong_answer',
            content={'wrong_answers': wrong_answers},
        )
        db.session.add(entry)
    if accuracy_rate < 0.7:
        entry = MemoryEntry(
            user_id=user_id,
            topic_id=topic_id,
            entry_type='weak_topic',
            content={'accuracy_rate': accuracy_rate},
        )
        db.session.add(entry)
    grammar_errors = [answer for answer in answers if answer.get('grammar_errors')]
    if grammar_errors:
        entry = MemoryEntry(
            user_id=user_id,
            topic_id=topic_id,
            entry_type='grammar_error',
            content={'errors': grammar_errors},
        )
        db.session.add(entry)
    db.session.commit()


def kullanici_hafiza_baglami_al(user_id, limit=20):
    entries = (
        MemoryEntry.query.filter_by(user_id=user_id)
        .order_by(MemoryEntry.created_at.desc())
        .limit(limit)
        .all()
    )
    topics = []
    for entry in entries:
        if entry.entry_type == 'weak_topic' and entry.topic_id:
            topics.append(entry.topic.slug if entry.topic else 'genel konu')
        elif entry.entry_type == 'grammar_error':
            topics.append('gramer')
        elif entry.entry_type == 'wrong_answer':
            topics.append('yanlış cevaplar')
    if not topics:
        return 'Kullanıcı henüz özel zayıf alan belirtmedi.'
    unique_topics = list(dict.fromkeys(topics))
    return 'Kullanıcı şunlarda zorlanıyor: ' + ', '.join(unique_topics)
