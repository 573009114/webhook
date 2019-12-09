import hashlib
import sys
import urllib
import requests
import time
import json

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
        send_data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "prometheus_alert",
                "text": "Alarm procedure: prometheus_alert \n" +
                        "*Alarm level*: %s \n\n" % content['labels']['severity'] +
                        "*Problem pod*: %s \n\n" % content['pod'] +
                        "*namespace*: %s \n\n" % content['namespace'] +
                        "*Alarm describe*: %s \n\n" % content['description'] +
                        "*Start time*: %s \n\n" % arrow.get(content['startsAt']).to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss ZZ') +
                        "*End time*: %s \n" % arrow.get(content['endsAt']).to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss ZZ')
            }
         }

        for mobile in mobileToList:
            data = {'sn':'DXX-BBX-103-20384','pwd':pwd,'mobile':mobile,'content':send_data.encode('gbk')}
            body = urllib.urlencode(data)
            request = requests.get(URL,body)
        return 'success'

@app.route('/send', methods=['POST'])
def send():
    data=json.loads(request.get_data())
    mobilelist=data['mobile']
    alerts=data['alerts']
    for content in alerts:
        try:
            result=sendsms(mobilelist,content)
            return result
        except TypeError:
            return 'sms type error'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
