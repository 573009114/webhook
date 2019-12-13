# -*- coding: UTF-8 -*-
import os
import json
import requests
import arrow

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def send():
    if request.method == 'POST':
        post_data = request.get_data()
        send_alert(bytes2json(post_data))
        return 'success'
    else:
        return 'weclome to use prometheus alertmanager dingtalk webhook server!'


def bytes2json(data_bytes):
    data = data_bytes.decode('utf8').replace("'", '"')
    return json.loads(data)


def send_alert(data):
    token ='e37d62c5a8b77360418317e40aae39ed8e50d566c53198e73349d0fba4609da1'
    if not token:
        print('you must set ROBOT_TOKEN env')
        return
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % token
    headers={
        'content-type': "application/json",
        'cache-control': "no-cache"
    }
    for alert in data["alerts"][:]:
        try:
            job=(alert["labels"]["job"])
        except Exception:
            job="nil"
        try:
            namespace=(alert["labels"]["namespace"])
        except Exception:
            namespace="nil"
        try:
            pod=(alert["labels"]["pod"])
        except Exception:
            pod="nil"
        try:
            alertname=(alert["labels"]["alertname"])
        except Exception:
            alertname="nil"
        try:
            instance=(alert["labels"]["instance"])
        except Exception:
            instance="nil"
        try:
            severity=(alert["labels"]["severity"])
        except Exception:
            severity="nil"
        try:
            service=(alert["labels"]["service"])
        except Exception:
            service="nil"
        try:
            deployment=(alert["labels"]["deployment"])
        except Exception:
            deployment="nil"
        try:
            message=(alert["annotations"]["message"])
        except Exception:
            message="nil"
        strtime=arrow.get(alert["startsAt"]).to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss ZZ')
        endtime=arrow.get(alert["endsAt"]).to('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss ZZ')
        status=alert["status"]

        data_format='''
           "开始时间: {strtime}"
           "结束时间: {endtime}"
           "告警状态: {status}"
           "告警名称: {alertname}"
           "故障级别: {severity}"
           "POD名: {pod}"
           "命名空间: {namespace}"
           "告警详情: {message}"'''.format(strtime=strtime,endtime=endtime,status=status,alertname=alertname,\
                                           namespace=namespace,message=message,severity=severity,pod=pod)

        send_data = {
            "msgtype": "text",
            "text": {
                "title": "Prometheus Alert",
                "content": data_format
            }
        }

        req = requests.post(url, json=send_data,verify=False,headers=headers)
        result = req.json()
        if result['errcode'] != 0:
            print('notify dingtalk error: %s' % result['errcode'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
