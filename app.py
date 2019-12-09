import hashlib
import sys
import urllib
import requests
import time

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return '<h1>webhooks sms</h1>'

def sendsms(mobilelist,content):
        mobileToList=mobilelist.split(',')
        URL = 'http://sdk.entinfo.cn:8060/z_mdsmssend.aspx'
        m = hashlib.md5()
        m.update('DXX-BBX-103-20384055649')
        pwd = m.hexdigest().upper()
        content = '%s' % (content)
        for mobile in mobileToList:
            data = {'sn':'DXX-BBX-103-20384','pwd':pwd,'mobile':mobile,'content':content.encode('gbk')}
            body = urllib.urlencode(data)
            request = requests.get(URL,body)
        return 'success'

def send():
    data=json.loads(request.data)
    mobile=data['mobile']
    alerts=data['alerts']
    for output in alerts:
        try:
            sendsms(mobile,output)
        except Exception as e:
            return e

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)