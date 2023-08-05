import requests
from lixinapi.__config import *
import json

def ressetLogin(loginname,loginpwd):
    url=loginurl+'loginname=%s&loginpwd=%s'%(loginname,loginpwd)
    print(url)
    s=requests.get(url).json()
    state=s['State']
    if state=='1':
        print(s['Msg'])
    else:
        print(s['Msg'])
if __name__ == '__main__':

    thsLogin = ressetLogin("zhangq", "123")
#     if (thsLogin == 0 or thsLogin == -201):