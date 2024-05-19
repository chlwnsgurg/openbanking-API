import json,requests
import os, time, pickle

def get(auth_code=None):
    url= 'https://testapi.openbanking.or.kr/oauth/2.0/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'code': auth_code,
        'client_id': 'db435b83-9fd7-48e5-8f5f-92c937ffbe62',
        'client_secret': '8ed0dc65-287f-448f-8df2-df4717940c12',
        'redirect_uri': 'http://127.0.0.1:5000/',
        'grant_type': 'authorization_code'
    }
    resp = requests.post(url=url, data=data, headers=headers)
    res=json.loads(resp.text)
    exp = round(time.time_ns()/1000000)+int(res['expires_in'])*1000
    with open('token_res', 'wb') as file:    
        pickle.dump(res, file)
    with open('token_exp', 'wb') as file:    
        pickle.dump(exp, file)
    return

def refresh(refresh_token):
    url= 'https://testapi.openbanking.or.kr/oauth/2.0/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': 'db435b83-9fd7-48e5-8f5f-92c937ffbe62',
        'client_secret': '8ed0dc65-287f-448f-8df2-df4717940c12',
        'refresh_token': refresh_token,
        'scope': 'login inquiry transfer',
        'grant_type': 'refresh_token'
    }
    resp = requests.post(url=url, data=data, headers=headers)
    res=json.loads(resp.text)
    exp = round(time.time_ns()/1000000)+int(res['expires_in'])*1000
    with open('token_res', 'wb') as file:    
        pickle.dump(res, file)
    with open('token_exp', 'wb') as file:    
        pickle.dump(exp, file)
    return

if __name__ == '__main__':
    if os.path.exists('token_res') and os.path.exists('token_exp'):
        with open('token_res', 'rb') as file:
            res=pickle.load(file)
        with open('token_exp', 'rb') as file:
            exp=pickle.load(file)
            if exp < round(time.time_ns()/1000000):
                print('Token expired')
                print('Requesting New Token...')
                auth_code=input('auth_code: ')
                get(auth_code)
                print('Request Successful!')
            elif exp == round(time.time_ns()/1000000):
                print('Token will expire soon')
                print('Refreshing Token...')
                refresh(res['refresh_token'])
                print('Refresh Successful!')
            else:
                print('Token already exists')
                exit(0)
    else:
        print('Requesting New Token...')
        auth_code=input('auth_code: ')
        get(auth_code)
        print('Request Successful!')

