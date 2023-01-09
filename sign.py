#!/usr/bin/env python3
import http.client
import json
import os

import requests

session = requests.session()
# noinspection HttpUrlsUsage
session.headers = {
    'Origin': 'http://gzdk.gzisp.net',
    'Referer': 'http://gzdk.gzisp.net/',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Version/13.0.3 Mobile/15E148 Safari/604.1'
}


def get_student_id(url, token):
    return session.post(url + '/mobile/getData', {
        'token': token,
    }).json()['data']['user']['student']['id']


def get_internship_id(url, token):
    return session.post(url + '/mobile/plan/internship/find-stu-current-or-not-start-internship', {
        'token': token,
    }).json()['data']['internshipId']


# noinspection PyPep8Naming
def sign(url, token, studentId=None, internshipId=None, address='', x='', y='', trip=False, checkType='CHECKIN',
         content='', attachIds=''):
    if not studentId:
        studentId = get_student_id(url, token)
        print('studentId:', studentId)
    if not internshipId:
        internshipId = get_internship_id(url, token)
        print('internshipId:', internshipId)
    resp = session.post(url + '/mobile/process/stu-location/save', {
        'token': token,
        'isAbnormal': 0,  # 是否异常
        'checkType': checkType,  # 签到类型：CHECKIN 签到、SIGNOFF 签退
        'studentId': studentId,
        'locationX': x,
        'locationY': y,
        'scale': 16,
        'label': address,
        'mapType': 'baidu',
        'content': content,
        'isEvection': int(trip),  # 是否出差
        'internshipId': internshipId,  # 实习 id
        'attachIds': attachIds,  # 附件 id
    })
    code = resp.status_code
    if code != 200:
        try:
            status = http.HTTPStatus(code).phrase
        except ValueError:
            status = ''
        print('resp:', code, status, resp.text)
    return resp.json()


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
        if token:
            push_plus_notify(token, '慧职教签到', '```text\n' + msg + '\n```', 'markdown')

    try:
        data = sign(**config['sign'])
        print(data)
        m = data['msg']
        if not m:
            if data['code'] == 0 and data['success']:
                m = '签到成功！'
            else:
                m = json.dumps(data)
        notify(m)
    except Exception as e:
        notify('签到失败：' + str(e))


if __name__ == '__main__':
    main()
