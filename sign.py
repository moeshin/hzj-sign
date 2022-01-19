#!/usr/bin/env python3
import http.client
import json
import os
import time
import urllib.parse


def sign(token, address='', location='', trip=False):
    conn = http.client.HTTPConnection('gzdk.gzisp.net', 8082)
    conn.request('POST', '/sign/addSignIn?' + urllib.parse.urlencode({
        'SCALE': 18,
        'authorization': token,
        'ISEVECTION': int(trip),
        'ADDR': address,
        'AXIS': location,

        # 以下参数可有可无
        'CONTENT': '',
        'IDS': '',
        'token': token,
        'time': int(time.time() * 1000),
    }))
    res = conn.getresponse()
    body = res.read()
    try:
        if json.loads(body).get('res') == 'success':
            return
    except json.decoder.JSONDecodeError:
        pass
    code = res.getcode()
    try:
        status = http.HTTPStatus(code).phrase
    except ValueError:
        status = ''
    raise Exception('%d %s\n%s' % (code, status, str(body, 'utf-8')))


def push_plus_notify(token, title, content, template='html'):
    body = json.dumps(locals())
    conn = http.client.HTTPSConnection('www.pushplus.plus')
    conn.request('POST', '/send/', body)
    res = conn.getresponse()
    body = res.read()
    try:
        if json.loads(body).get('code') == 200:
            return
    except json.decoder.JSONDecodeError:
        pass
    code = res.getcode()
    try:
        status = http.HTTPStatus(code).phrase
    except ValueError:
        status = ''
    print('PushPlus 通知失败：%d %s\n%s' % (code, status, str(body, 'utf-8')))


def main():
    config_path = os.path.dirname(os.path.abspath(__file__)) + '/config.json'
    try:
        with open(config_path, encoding='utf-8') as fp:
            config = json.load(fp)
    except FileNotFoundError:
        print("配置文件不存在：%s" % config_path)
        exit(1)

    def notify(msg):
        print(msg)
        token = config.get('pushplus')
        if token is not None:
            push_plus_notify(token, '慧职教签到', '```text\n' + msg + '\n```', 'markdown')

    try:
        sign(config['token'], config.get('address', ''), config.get('location', ''), config.get('trip', False))
        notify('签到成功！')
    except Exception as e:
        notify('签到失败：' + str(e))


if __name__ == '__main__':
    main()
