import urllib.request
import urllib.error
import json

url = 'http://127.0.0.1:5000'
req_data = json.dumps({'name': 'TestUserAI2', 'email': 'testuserai2+copilot@example.com', 'password': 'Password123'}).encode('utf-8')
req = urllib.request.Request(f'{url}/api/auth/kayit', data=req_data, headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req)
content = resp.read().decode('utf-8')
print('REGISTER', resp.status, content)
obj = json.loads(content)
token = obj['data']['access_token']
print('TOKEN', token)
for path in ['/api/auth/ben', '/api/ogrenme/konular', '/api/ai/soru-uret']:
    body = None
    if path == '/api/ai/soru-uret':
        body = json.dumps({'topic_id': 1, 'count': 1, 'types': ['multiple_choice']}).encode('utf-8')
    req = urllib.request.Request(f'{url}{path}', data=body, headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'})
    try:
        r = urllib.request.urlopen(req)
        print(path, r.status, r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(path, 'ERROR', e.code)
        print(e.read().decode('utf-8'))
