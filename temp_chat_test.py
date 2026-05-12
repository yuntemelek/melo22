import json
import urllib.request
import urllib.error

url = 'http://127.0.0.1:5000'

for email in ['testuserai2+copilot@example.com', 'testuserai2@example.com']:
    try:
        data = json.dumps({'name':'TestUserAI','email':email,'password':'Password123'}).encode('utf-8')
        req = urllib.request.Request(f'{url}/api/auth/kayit', data=data, headers={'Content-Type':'application/json'})
        resp = urllib.request.urlopen(req)
        obj = json.loads(resp.read().decode('utf-8'))
        token = obj['data']['access_token']
        print('REGISTERED', email)
        break
    except urllib.error.HTTPError as e:
        content = e.read().decode('utf-8')
        print('REGISTER ERROR', e.code, content)
        if 'email' in content:
            try:
                data = json.dumps({'email':email,'password':'Password123'}).encode('utf-8')
                req = urllib.request.Request(f'{url}/api/auth/giris', data=data, headers={'Content-Type':'application/json'})
                resp = urllib.request.urlopen(req)
                obj = json.loads(resp.read().decode('utf-8'))
                token = obj['data']['access_token']
                print('LOGGED IN', email)
                break
            except Exception as e2:
                print('LOGIN FAILED', e2)
                token = None
                break
        token = None
if not token:
    raise SystemExit('No token')
print('TOKEN', token[:20] + '...')

for path, payload in [
    ('/api/auth/ben', None),
    ('/api/ogrenme/konular', None),
    ('/api/ai/soru-uret', {'topic_id':1,'count':1,'types':['multiple_choice']}),
    ('/api/ai/sohbet', {'messages':[{'role':'user','content':'Hello'}],'session_id':None}),
]:
    data = None
    if payload is not None:
        data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(f'{url}{path}', data=data, headers={'Content-Type':'application/json','Authorization':f'Bearer {token}'})
    try:
        resp = urllib.request.urlopen(req)
        body = resp.read().decode('utf-8')
        print(path, resp.status, body[:1000])
    except urllib.error.HTTPError as e:
        print(path, 'ERROR', e.code, e.read().decode('utf-8'))
    except Exception as e:
        print(path, 'EXCEPTION', e)
