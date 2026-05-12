import os
from pathlib import Path
from flask import Flask, send_from_directory, jsonify
from dotenv import load_dotenv
from extensions import db, jwt, cors
from config import DevelopmentConfig, ProductionConfig
from routes.auth import auth_bp
from routes.user import user_bp
from routes.learning import learning_bp
from routes.ai import ai_bp
from models import User, Topic

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

CONFIG_MAP = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

TOPIC_SEED = [
    {
        'slug': 'present-simple',
        'title_tr': 'Present Simple',
        'description_tr': 'Günlük alışkanlıklar ve rutinler için temel zaman.',
        'level': 'A1',
    },
    {
        'slug': 'present-continuous',
        'title_tr': 'Present Continuous',
        'description_tr': 'Şu anda devam eden eylemler için kullanılır.',
        'level': 'A2',
    },
    {
        'slug': 'past-simple',
        'title_tr': 'Past Simple',
        'description_tr': 'Geçmişte tamamlanmış olayları anlatmak için.',
        'level': 'A2',
    },
    {
        'slug': 'future-simple',
        'title_tr': 'Future Simple',
        'description_tr': 'Gelecek planlar ve tahminler için temel ifade.',
        'level': 'B1',
    },
    {
        'slug': 'present-perfect',
        'title_tr': 'Present Perfect',
        'description_tr': 'Geçmişten bugüne bağlantı kuran durumlar.',
        'level': 'B2',
    },
    {
        'slug': 'conditional-type-1',
        'title_tr': 'Type 1 Conditional',
        'description_tr': 'Gerçekçi koşullar ve olası sonuçlar.',
        'level': 'B2',
    },
]


def create_app(config_name: str = None):
    app = Flask(
        __name__,
        static_folder=str(BASE_DIR / '..' / 'frontend' / 'dist'),
        static_url_path='/',
    )
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(CONFIG_MAP.get(config_name, DevelopmentConfig))

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/kullanici')
    app.register_blueprint(learning_bp, url_prefix='/api/ogrenme')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')

    with app.app_context():
        db.create_all()
        for topic_payload in TOPIC_SEED:
            if not Topic.query.filter_by(slug=topic_payload['slug']).first():
                topic = Topic(**topic_payload)
                db.session.add(topic)
        db.session.commit()

    @app.errorhandler(404)
    def not_found(error):
        index_path = Path(app.static_folder) / 'index.html'
        if index_path.exists():
            return send_from_directory(app.static_folder, 'index.html')
        return jsonify({'success': False, 'data': None, 'error': 'Route bulunamadı.'}), 404

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        target = Path(app.static_folder) / path
        if path and target.exists():
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'index.html')

    return app
