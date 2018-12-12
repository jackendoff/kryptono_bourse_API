import hashlib
import hmac
import http.client as http
import json
import logging
import time
import urllib
from content import api_key,secret_key

'''
根据密匙生成签名
'''


class Kryptono(object):

    # 构造器
    def __init__(self, api_key, secrect_key):
        self.api_key = api_key
        self.secrect_key = secrect_key.encode("UTF-8")

    # 发送服务器请求
    def __send(self, method, path, data={}):

        headers = {}
        data_str = ""
        body = ""
        signature = ""

        if method == "GET":
            data_str = urllib.parse.urlencode(data)
            path += "?" + data_str
        elif method == "POST":
            data_str = json.dumps(data)
            body = data_str

        signature = hmac.new(self.secrect_key, data_str.encode("UTF-8"), hashlib.sha256).hexdigest()

        # 编辑header完成身份验证
        headers["Accept"] = "application/json"
        headers["Authorization"] = self.api_key
        headers["Signature"] = signature
        headers["X-Requested-With"] = "XMLHttpRequest"
        if not method == 'GET':
            headers["Content-Type"] = 'application/json'

        # self.logger.debug("Kryptono请求数据:[%s][%s][%s]", "/k" + path, body, headers)

        # 发送请求
        conn = http.HTTPSConnection("p.kryptono.exchange")
        try:
            conn.request(method, "/k" + path, body, headers)
        except:
            # self.logger.exception('Kryptono服务器暂时不可用')
            raise Exception()

        resp = conn.getresponse()
        resp_text = resp.read().decode('UTF-8')

        if resp.status != 200:
            # self.logger.error("Kryptono请求失败:[%s]", resp_text)
            raise Exception()

        # self.logger.debug("Kryptono请求结果:[%s]", resp_text)
        return resp_text


if __name__ == '__main__':
    kryptono = Kryptono(api_key,secret_key)

