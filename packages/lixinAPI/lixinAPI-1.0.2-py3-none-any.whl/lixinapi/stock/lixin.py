import requests
import json
from lixinapi.__config import *

def ressetLogin(loginname,loginpwd):
    url=loginurl%(loginname,loginpwd)
    # print(url)
    s=requests.get(url).json()
    state=str(s['State'])
    if state=='1':
        print(s['Msg'])
    else:
        print(s['Msg'])

def get_history_data(security,startdate='',enddate=''):
    url=stockurl%(security,startdate,enddate)
    # print(url)
    s=requests.get(url).json()
    state=str(s['State'])
    if state=='1':
        return s['Data']
    else:
        print(s['Msg'])

def get_Income_data(security,startdate='',enddate=''):
    url=incomeurl%(security,startdate,enddate)
    # print(url)
    s=requests.get(url).json()
    state=str(s['State'])
    if state=='1':
        print(s['Data'])
    else:
        print(s['Msg'])

def get_CashFlow_data(security,startdate='',enddate=''):
    url=cashflowurl%(security,startdate,enddate)
    # print(url)
    s=requests.get(url).json()
    state=str(s['State'])
    if state=='1':
        return s['Data']
    else:
        print(s['Msg'])

def get_Balance_data(security,startdate='',enddate=''):
    url=balanceurl%(security,startdate,enddate)
    # print(url)
    s=requests.get(url).json()
    state=str(s['State'])
    if state=='1':
        return s['Data']
    else:
        print(s['Msg'])

def get_Content_data(code,content_type, type, year):
    url=contenturl%(code, content_type,type, year)
    # print(url)
    s=requests.get(url).json()
    state=str(s['State'])
    if state=='1':
        return json.loads(s['Data']) ['response']['docs']
    else:
        print(s['Msg'])
if __name__ == '__main__':
    # s =get_Balance_data('83_600519,90_000001','2019-09-10','2021-09-16')
    s=get_Content_data('000001','part',  '年度报告', '2011')
    print(s)
    # thsLogin = ressetLogin("zhangq", "123")