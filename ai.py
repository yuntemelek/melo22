import json
from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import User
from models.learning import Topic
from models.chat import ChatSession, ChatMessage
from services.ai_service import AIService
from services.memory_service import kullanici_hafiza_baglami_al
from config import BaseConfig

ai_bp = Blueprint('ai', __name__)


def response(success, data=None, error=None, status=200):
    return jsonify({'success': success, 'data': data, 'error': error}), status


@ai_bp.route('/soru-uret', methods=['POST'])
@jwt_required()
def generate_questions():
    payload = request.get_json(force=True)
    topic_id = payload.get('topic_id')
    count = int(payload.get('count', 5))
    types = payload.get('types', ['multiple_choice', 'fill_blank', 'writing'])

    topic = Topic.query.get(topic_id)
    if not topic:
        return response(False, error='Konu bulunamadı.', status=404)

    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    try:
        memory_text = kullanici_hafiza_baglami_al(user_id)
        ai = AIService(BaseConfig())
        questions = ai.soru_uret(topic.title_tr, user.level or 'A1', count, types, memory_text)
        return response(True, data={'questions': questions})
    except Exception as exc:
        return response(False, error=str(exc) or 'AI soru üretimi sırasında bir hata oluştu.', status=500)


@ai_bp.route('/cevap-degerlendir', methods=['POST'])
@jwt_required()
def evaluate_answer():
    payload = request.get_json(force=True)
    question = payload.get('question')
    user_answer = payload.get('user_answer')
    if not question:
        return response(False, error='Soru verisi gerekli.', status=400)
    try:
        ai = AIService(BaseConfig())
        evaluation = ai.cevap_degerlendir(question, user_answer)
        return response(True, data={'evaluation': evaluation})
    except Exception as exc:
        return response(False, error=str(exc) or 'AI cevap değerlendirmesi sırasında bir hata oluştu.', status=500)


def _stream_events(generator):
    for chunk in generator:
        yield f'data: {chunk}\n\n'


@ai_bp.route('/sohbet', methods=['POST'])
@jwt_required()
def chat():
    payload = request.get_json(force=True)
    messages = payload.get('messages', [])
    session_id = payload.get('session_id')
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return response(False, error='Kullanıcı bulunamadı.', status=404)

    if session_id:
        session = ChatSession.query.filter_by(id=session_id, user_id=user_id).first()
        if not session:
            return response(False, error='Sohbet oturumu bulunamadı.', status=404)
        session_id_value = session.id
    else:
        session = ChatSession(user_id=user_id)
        db.session.add(session)
        db.session.flush()
        session_id_value = session.id
        db.session.commit()

    for message in messages:
        if message.get('role') in ['user', 'assistant']:
            msg = ChatMessage(session_id=session_id_value, role=message['role'], content=message['content'])
            db.session.add(msg)
    db.session.commit()

    memory_text = kullanici_hafiza_baglami_al(user_id)
    ai = AIService(BaseConfig())
    try:
        assistant_text = ai.sohbet(messages, user.to_dict(), memory_text)
    except Exception as exc:
        return response(False, error=str(exc) or 'Sohbet başlatılırken bir hata oluştu.', status=500)

    response_message = ChatMessage(session_id=session_id_value, role='assistant', content=assistant_text)
    db.session.add(response_message)
    db.session.commit()

    def event_stream():
        yield json.dumps({'type': 'session', 'session_id': session_id_value})
        for segment in assistant_text.split('\n'):
            yield json.dumps({'type': 'message', 'content': segment})

    return Response(_stream_events(event_stream()), mimetype='text/event-stream')


@ai_bp.route('/sohbet/gecmis', methods=['GET'])
@jwt_required()
def chat_history():
    user_id = int(get_jwt_identity())
    sessions = ChatSession.query.filter_by(user_id=user_id).order_by(ChatSession.created_at.desc()).limit(20).all()
    data = [
        {'id': session.id, 'created_at': session.created_at.isoformat(), 'message_count': len(session.messages)}
        for session in sessions
    ]
    return response(True, data={'sessions': data})


@ai_bp.route('/sohbet/<int:session_id>', methods=['GET'])
@jwt_required()
def chat_session(session_id):
    user_id = int(get_jwt_identity())
    session = ChatSession.query.filter_by(id=session_id, user_id=user_id).first()
    if not session:
        return response(False, error='Sohbet oturumu bulunamadı.', status=404)
    return response(True, data={'session': session.to_dict()})


@ai_bp.route('/konu-oner', methods=['POST'])
@jwt_required()
def suggest_topic():
    payload = request.get_json(force=True)
    session_id = payload.get('session_id')
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return response(False, error='Kullanıcı bulunamadı.', status=404)
    session = ChatSession.query.filter_by(id=session_id, user_id=user_id).first()
    if not session:
        return response(False, error='Sohbet oturumu bulunamadı.', status=404)
    messages = [{'role': message.role, 'content': message.content} for message in session.messages]
    ai = AIService(BaseConfig())
    try:
        suggestion = ai.konu_oner(messages, user.level or 'A1')
        return response(True, data={'suggestion': suggestion})
    except Exception as exc:
        return response(False, error=str(exc) or 'Konu önerisi oluşturulurken bir hata oluştu.', status=500)
