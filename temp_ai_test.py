import urllib.request
import urllib.error
import json

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3ODU1MDM5MywianRpIjoiODg4MjJlNTktNzY2ZS00N2IyLTk0MDYtOGZhZWY1MDkzMzAxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjgiLCJuYmYiOjE3Nzc4NTUwMzkzLCJleHAiOjE3Nzc4NTUxMjkzfQ.F4xIfycS4T3hDCzhpUoPcf0QbESHoQmpNZRJHaxtobo"
body = json.dumps({'topic_id': 1, 'count': 5, 'types': ['multiple_choice', 'fill_blank', 'writing']}).encode('utf-8')
req = urllib.request.Request(
    'http://127.0.0.1:5000/api/ai/soru-uret',
    data=body,
    headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
)
try:
    r = urllib.request.urlopen(req)
    print(r.status)
    print(r.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print('ERR', e.code)
    print(e.read().decode('utf-8'))
