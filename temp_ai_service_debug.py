import json
from services.ai_service import AIService
from config import BaseConfig

service = AIService(BaseConfig())
try:
    questions = service.soru_uret('Present Simple', 'A1', 3, ['multiple_choice', 'fill_blank', 'writing'], 'Kullanıcı zayıf alanları yok')
    print('QUESTIONS', questions)
except Exception as e:
    print('ERROR', type(e).__name__, str(e))
    import traceback
    traceback.print_exc()
