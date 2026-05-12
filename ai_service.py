import json
import time
import openai
from config import BaseConfig

class AIService:
    def __init__(self, config: BaseConfig):
        openai.api_key = config.OPENAI_API_KEY
        self.model = config.OPENAI_MODEL

    def _retry(self, func, *args, **kwargs):
        attempts = 0
        while attempts < 3:
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                attempts += 1
                if attempts >= 3:
                    raise
                time.sleep(2 ** attempts)

    def soru_uret(self, topic, level, count, types, user_memory):
        system_prompt = (
            'Sen bir İngilizce öğretmenisin. Türkçe bilen ' + level + ' seviyesi öğrenciler için '
            'İngilizce soruları şu formatta üret. '
            'Kullanıcının zayıf alanları: ' + user_memory + '\n'
            'Konu: ' + topic + '\n'
            'Soru sayısı: ' + str(count) + '\n'
            'Soru tipleri: ' + ', '.join(types) + '\n\n'
            'YALNIZCA şu JSON array\'i döndür, başka hiçbir şey yazma:\n'
            '[\n'
            '  {\n'
            '    "id": "uuid",\n'
            '    "type": "multiple_choice" | "fill_blank" | "writing",\n'
            '    "question": "İngilizce veya Türkçe soru metni",\n'
            '    "options": ["A", "B", "C", "D"],\n'
            '    "correct_answer": "doğru cevap",\n'
            '    "explanation_tr": "Türkçe açıklama"\n'
            '  }\n'
            ']'
        )
        body = [
            {'role': 'system', 'content': system_prompt},
            {
                'role': 'user',
                'content': 'Lütfen soruları JSON formatında üretin.',
            },
        ]
        response = self._retry(
            openai.ChatCompletion.create,
            model=self.model,
            messages=body,
            temperature=0.6,
            max_tokens=850,
        )
        raw = response.choices[0].message.content.strip()
        try:
            questions = json.loads(raw)
        except json.JSONDecodeError:
            raise ValueError('AI yanıtı JSON olarak alınamadı.')
        return questions

    def cevap_degerlendir(self, question, user_answer):
        system_prompt = (
            'Kullanıcının cevabını değerlendir.\n'
            'Soru: ' + question.get('question', '') + '\n'
            'Kullanıcının cevabı: ' + str(user_answer) + '\n'
            'Doğru cevap: ' + str(question.get('correct_answer', '')) + '\n\n'
            'YALNIZCA JSON döndür:\n'
            '{\n'
            '  "correct": true/false,\n'
            '  "explanation_tr": "Türkçe açıklama",\n'
            '  "grammar_errors": [{ "wrong": "x", "correct": "y", "note_tr": "açıklama" }]\n'
            '}'
        )
        body = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': 'Lütfen sadece JSON olarak yanıtlayın.'},
        ]
        response = self._retry(
            openai.ChatCompletion.create,
            model=self.model,
            messages=body,
            temperature=0,
            max_tokens=350,
        )
        raw = response.choices[0].message.content.strip()
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            raise ValueError('AI yanıtı JSON olarak alınamadı.')

    def sohbet(self, messages, user_profile, user_memory):
        system_prompt = (
            """
Sen Melo'nun AI İngilizce öğretmenisin. Kullanıcıyla Türkçe konuşabilirsin ama
İngilizce öğretmek için buradayız.

Kullanıcı: %s, Seviye: %s
Zayıf alanlar: %s

Kurallar:
- Kullanıcı İngilizce yazarsa hataları [HATA: X → DOĞRUSU: Y] formatında göster
- Samimi, motive edici bir öğretmen ol
- Sohbet akışını bozmadan düzelt
- Her 5 mesajda bir, sohbetten tespit ettiğin zayıf konuyu öner:
  <KONU_ONERISI>{ "slug": "...", "title_tr": "...", "reason_tr": "..." }</KONU_ONERISI>
"""
            % (
                user_profile.get('name', ''),
                user_profile.get('level', ''),
                user_memory,
            )
        )
        body = [
            {'role': 'system', 'content': system_prompt},
        ]
        body.extend(messages)
        response = self._retry(
            openai.ChatCompletion.create,
            model=self.model,
            messages=body,
            temperature=0.8,
            max_tokens=800,
        )
        return response.choices[0].message.content

    def konu_oner(self, chat_messages, user_level):
        system_prompt = (
            'Bu sohbet geçmişini analiz et ve kullanıcının pratik etmesi gereken '
            'en önemli İngilizce konusunu belirle.\n\n'
            'YALNIZCA JSON döndür:\n'
            '{\n'
            '  "slug": "present-perfect",\n'
            '  "title_tr": "Present Perfect Tense",\n'
            '  "reason_tr": "Sohbette present perfect kullanımında hatalar tespit edildi"\n'
            '}'
        )
        body = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': json.dumps({'messages': chat_messages, 'level': user_level}, ensure_ascii=False)},
        ]
        response = self._retry(
            openai.ChatCompletion.create,
            model=self.model,
            messages=body,
            temperature=0.3,
            max_tokens=250,
        )
        raw = response.choices[0].message.content.strip()
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            raise ValueError('AI önerisi JSON olarak alınamadı.')
