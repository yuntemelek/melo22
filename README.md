# Melo — AI Destekli İngilizce Öğrenme Platformu

Melo, Türkçe bilen kullanıcılar için tasarlanmış AI destekli bir İngilizce öğrenme platformudur. Bu proje, React + Vite + Tailwind tabanlı frontend ile Flask + SQLAlchemy + OpenAI destekli backend içerir.

## Proje Yapısı

```
melo/
  frontend/
  backend/
  README.md
```

## Backend Kurulumu

1. `cd backend`
2. `python -m venv venv`
3. `venv\Scripts\activate`
4. `pip install -r requirements.txt`
5. `.env` dosyasını oluşturun ve `.env.example` içeriğini kopyalayın.
6. `flask run`

Backend varsayılan olarak `http://127.0.0.1:5000` üzerinde çalışır.

### PythonAnywhere Deploy

`backend/pythonanywhere_wsgi.py` dosyasında kullanıcı adı ve yol bilgilerini güncelleyin.

`config.py` içinde `ProductionConfig` kısmında aşağıdaki ayarları kullanabilirsiniz:

- `DATABASE_URL = sqlite:////home/KULLANICI_ADI/melo/backend/melo_prod.db`
- `DEBUG = False`
- `CORS_ORIGINS = ['https://KULLANICI_ADI.pythonanywhere.com']`

## Frontend Kurulumu

1. `cd frontend`
2. `npm install`
3. `npm run dev`

Frontend, `http://localhost:4173` üzerinde çalışacak şekilde konfigüre edilmiştir.

## Önemli Özellikler

- JWT tabanlı kimlik doğrulama
- LocalStorage destekli sohbet geçmişi
- AI destekli sorular ve cevap değerlendirme
- Sayfa geçiş animasyonları
- Tailwind özel renk tokenları
- Flask backend üzerinde SPA yakalama rotası

## Notlar

- Tüm gizli anahtarlar `.env` içinde tutulur.
- Frontend `VITE_API_BASE_URL` olarak `/api` kullanır.
- Backend `CORS_ORIGINS` environment variable üzerinden ayarlanır.
