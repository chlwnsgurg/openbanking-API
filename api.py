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
    idx=int(input('Choose Account>'))
    return res['res_list'][idx-1]

def api():
        global account,account_info
        global fintech_use_num
        idx
        idx-=1
        account_name=account[idx]
        fintech_use_num=account_info[idx]['fintech_use_num']

def balance():
    global access_token,user_seq_no
    global fintech_use_num
    url= 'https://testapi.openbanking.or.kr/v2.0/account/balance/fin_num'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    params = {
            'bank_tran_id': 'M202401128'+'U'+str(round(time.time()/10)),
            'fintech_use_num': fintech_use_num,
            'tran_dtime': time.strftime('%Y%m%d%H%M%S')
    }
    response = requests.get(url=url, params=params, headers=headers)
    result=json.loads(response.text)
    return result


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
                    for idx,info in enumerate(account):
                        print(str(idx+1)+'.',info)
                    api()
                elif choice == '2':
                    print('거래내역조회')
                    for idx,info in enumerate(account):
                        print(str(idx+1)+'.',info)
                    balance()
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