import json,requests
import os, time, pickle

client_use_code='M202401128'

def info(access_token,user_seq_no):
    url= 'https://testapi.openbanking.or.kr/v2.0/account/list'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    params = {
            'user_seq_no': user_seq_no,
            'include_cancel_yn': 'N',
            'sort_order': 'D'
    }
    resp=requests.get(url=url, params=params, headers=headers)
    res=json.loads(resp.text)
    print('Account List')
    for i,info in enumerate(res['res_list']):
        print(str(i+1)+') '+info['bank_name']+' '+info['account_num_masked']+' - '+info['account_holder_name'])
    idx=int(input('Choose Account:'))
    return res['res_list'][idx-1]

def balance(access_token,fintech_use_num):
    url= 'https://testapi.openbanking.or.kr/v2.0/account/balance/fin_num'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    params = {
            'bank_tran_id': client_use_code+'U'+str(round(time.time())%int(1e9)),
            'fintech_use_num': fintech_use_num,
            'tran_dtime': time.strftime('%Y%m%d%H%M%S')
    }
    response = requests.get(url=url, params=params, headers=headers)
    result=json.loads(response.text)
    print(result)
    return

def transaction(from_date,to_date, access_token,fintech_use_num):
    url= 'https://testapi.openbanking.or.kr/v2.0/account/transaction_list/fin_num'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    params = {
            'bank_tran_id': client_use_code+'U'+str(round(time.time())%int(1e9)),
            'fintech_use_num': fintech_use_num,
            'inquiry_type' : 'A',
            'inquiry_base' : 'D',
            'from_date' : from_date,
            'to_date' : to_date,
            'sort_order' : 'D',
            'tran_dtime': time.strftime('%Y%m%d%H%M%S')
    }
    response = requests.get(url=url, params=params, headers=headers)
    result=json.loads(response.text)
    print(result)
    return



if __name__ == '__main__':
    if os.path.exists('token_res') and os.path.exists('token_exp'):
        with open('token_res', 'rb') as file:
            res=pickle.load(file)
        with open('token_exp', 'rb') as file:
            exp=pickle.load(file)
        if exp > round(time.time_ns()/1000000):
            access_token=res['access_token']
            user_seq_no=res['user_seq_no']
            print('Requesting Account Information...')
            account_info=info(access_token,user_seq_no)
            fintech_use_num=account_info['fintech_use_num']
            print('Request Successful!')
            while True:
                print('1) 잔액조회')
                print('2) 거래내역조회')
                print('3) Exit')
                choice=input('Select> ')
                if choice == '1':
                    print('잔액조회')
                    balance(access_token,fintech_use_num)
                elif choice == '2':
                    print('거래내역조회')
                    from_date=input('조회 시작 일자(YYYYMMDD): ')
                    to_date=input('조회 종료 일자(YYYYMMDD): ')
                    transaction(from_date,to_date, access_token,fintech_use_num)
                elif choice == '3':
                    break
                else:
                    print('Invalid Input')
        else:
            print('Token expired')
            print('Execute jwt.py')
    else:
        print('Token does not exist')
        print('Execute jwt.py')