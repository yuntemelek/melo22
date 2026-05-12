import bcrypt
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from extensions import db
from models.user import User

auth_bp = Blueprint('auth', __name__)


def response(success, data=None, error=None, status=200):
    return jsonify({'success': success, 'data': data, 'error': error}), status


@auth_bp.route('/kayit', methods=['POST'])
def register():
    payload = request.get_json(force=True)
    email = payload.get('email', '').strip().lower()
    password = payload.get('password', '')
    name = payload.get('name', '').strip()

    if not email or '@' not in email:
        return response(False, error='Geçerli bir e-posta girin.', status=400)
    if len(password) < 8:
        return response(False, error='Şifre en az 8 karakter olmalıdır.', status=400)
    if User.query.filter_by(email=email).first():
        return response(False, error='Bu e-posta zaten kayıtlı.', status=400)

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
    user = User(email=email, password_hash=hashed.decode('utf-8'), name=name or None)
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return response(True, data={'access_token': access_token, 'refresh_token': refresh_token, 'user': user.to_dict()})


@auth_bp.route('/giris', methods=['POST'])
def login():
    payload = request.get_json(force=True)
    email = payload.get('email', '').strip().lower()
    password = payload.get('password', '')

    if not email or not password:
        return response(False, error='E-posta ve şifre gerekli.', status=400)
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return response(False, error='E-posta veya şifre yanlış.', status=401)

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return response(True, data={'access_token': access_token, 'refresh_token': refresh_token, 'user': user.to_dict()})


@auth_bp.route('/cikis', methods=['POST'])
@jwt_required()
def logout():
    return response(True, data={'message': 'Çıkış yapıldı.'})


@auth_bp.route('/ben', methods=['GET'])
@jwt_required()
def whoami():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return response(False, error='Kullanıcı bulunamadı.', status=404)
    return response(True, data={'user': user.to_dict()})


@auth_bp.route('/yenile', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=str(user_id))
    return response(True, data={'access_token': access_token})
