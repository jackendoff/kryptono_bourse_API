# coding=utf-8
from content import api_key, secret_key
import hashlib
import hmac
import http.client as http
import json
import logging
import time
import urllib
import pandas as pd


 # from conf import BITMEX

# Kryptono交易所


class Kryptono(object):

    # 构造器
    def __init__(self, api_key, secrect_key):
        # self.logger = logging.getLogger("quant.kryptono")
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
        elif method == "DELETE":
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
        # print('resp:',resp)
        # print('resp_text:',resp_text,resp.status)
        if resp.status != 200:
            print("Kryptono请求失败:[%s]", resp_text)
            raise Exception()

        # self.logger.debug("Kryptono请求结果:[%s]", resp_text)
        return resp_text

    def new_order(self,order_symbol,order_side,order_price,order_size,type,stop_price=None,recvWindow=None):
        '''
        创建新的订单,目前测试
        :param order_symbol:
        :param order_side:
        :param order_price:
        :param order_size:
        :param type:
        :param stop_price:
        :param recvWindow:
        :return:
        '''
        data = {}
        data['order_symbol'] = order_symbol
        data['order_side'] = order_side
        data['order_price'] = order_price
        data['order_size'] = order_size
        data['type'] = type
        if not stop_price is None: data['stop_price'] = stop_price
        if not recvWindow is None: data['recvWindow'] = recvWindow
        else:data['recvWindow'] = 5000
        data['timestamp'] = int(time.time()) * 1000
        print(data)
        def re_get():
            try:
                global resp
                resp = self.__send("POST", '/api/v2/order/add', data)
            except:
                print("Kryptono获取所有历史数据失败")
                re_get()
            return resp
        resp = re_get()
        # print(resp)
        resp_json = json.loads(resp)
        # if not isinstance(resp_json, list):
        #     # self.logger.error("Kryptono获取所有历史数据失败:[%s]", resp)
        #     return

        return resp_json

    def cancel_order(self,order_id,order_symbol,recvWindow=None):
        '''
        #取消订单
        :param order_id:
        :param order_symbol:
        :param recvWindow:
        :return:
        '''
        data = {}
        data['order_id'] = order_id
        data['order_symbol'] = order_symbol
        if not recvWindow is None:
            data['recvWindow'] = recvWindow
        else:
            data['recvWindow'] = 5000
        data['timestamp'] = int(time.time()) * 1000
        # print(data)
        def re_get():
            try:
                global resp
                resp = self.__send("DELETE", '/api/v2/order/cancel', data)
            except:
                print("Kryptono获取所有历史数据失败")
                re_get()
            return resp
        resp = re_get()
        print(resp)
        resp_json = json.loads(resp)
        # if not isinstance(resp_json, list):
        #     # self.logger.error("Kryptono获取所有历史数据失败:[%s]", resp)
        #     return

        return resp_json

    def get_trade_detail(self,order_id,recvWindow=None):
        #获取交易详情
        data = {}
        data['order_id'] = order_id
        if not recvWindow is None:
            data['recvWindow'] = recvWindow
        else:
            data['recvWindow'] = 5000
        data['timestamp'] = int(time.time()) * 1000
        # print(data)

        try:
            resp = self.__send("POST", '/api/v2/order/trade-detail', data)
        except:
            # self.logger.error("Kryptono获取所有历史数据失败")
            return
        print(resp)
        resp_json = json.loads(resp)
        if not isinstance(resp_json, list):
            # self.logger.error("Kryptono获取所有历史数据失败:[%s]", resp)
            return

        return resp_json
        pass

    def order_detail(self,order_id,recvWindow=None):
        '''
        获取订单明细
        :param order_id:
        :param recvWindow:
        :return:
        '''
        data = {}
        data['order_id'] = order_id
        if not recvWindow is None:
            data['recvWindow'] = recvWindow
        else:
            data['recvWindow'] = 5000
        data['timestamp'] = int(time.time()) * 1000
        # print('data:',data)
        def re_get():
            try:
                global resp
                resp = self.__send("POST", '/api/v2/order/details', data)
            except:
                print("Kryptono获取所有历史数据失败")
                re_get()
            return resp
        resp = re_get()
        # print(resp)
        resp_json = json.loads(resp)
        # if not isinstance(resp_json, list):
        #     # self.logger.error("Kryptono获取所有历史数据失败:[%s]", resp)
        #     return

        return resp_json

        pass

    def get_open_orders(self,symbol,limit=None,page=None,recvWindow=None):
        #获取未结订单
        data = {}
        data['symbol'] = symbol
        if not limit is None:
            data['limit'] = limit
        if not page is None:
            data['page'] = page
        if not recvWindow is None:
            data['recvWindow'] = recvWindow
        else:
            data['recvWindow'] = 5000
        data['timestamp'] = int(time.time()) * 1000
        # print('data:', data)
        def re_get():
            try:
                global resp
                resp = self.__send("POST", '/api/v2/order/list/open', data)
            except:
                print("Kryptono获取所有历史数据失败")
                re_get()
            return resp
        resp = re_get()
        # print(resp)
        resp_json = json.loads(resp)
        # if not isinstance(resp_json, list):
        #     # self.logger.error("Kryptono获取所有历史数据失败:[%s]", resp)
        #     return

        return resp_json
        pass

    def get_completed_orders(self,symbol,limit=None,page=None,recvWindow=None):
        #获取完成订单。1000个
        data = {}
        data['symbol'] = symbol
        if not limit is None:
            data['limit'] = limit
        if not page is None:
            data['page'] = page
        if not recvWindow is None:
            data['recvWindow'] = recvWindow
        else:
            data['recvWindow'] = 5000
        data['timestamp'] = int(time.time()) * 1000
        # print('data:', data)
        def re_get():
            try:
                global resp
                resp = self.__send("POST", '/api/v2/order/list/completed', data)
            except:
                print("Kryptono获取所有历史数据失败")
                re_get()
            return resp
        resp = re_get()
        # print(resp)
        resp_json = json.loads(resp)
        # print(resp_json)
        # if not isinstance(resp_json, list):
        #     # self.logger.error("Kryptono获取所有历史数据失败:[%s]", resp)
        #     return

        return resp_json
        pass

    def get_all_orders(self,symbol,from_id=None,limit=None,recvWindow=None):
        '''
        #获取所有订单
        :param symbol:
        :param from_id:
        :param limit:
        :param recvWindow:
        :return:
        '''
        data = {}
        data['symbol'] = symbol
        if not limit is None:
            data['limit'] = limit
        if not from_id is None:
            data['page'] = from_id
        if not recvWindow is None:
            data['recvWindow'] = recvWindow
        else:
            data['recvWindow'] = 5000
        data['timestamp'] = int(time.time()) * 1000
        # print('data:', data)
        def re_get():
            try:
                global resp
                resp = self.__send("POST", '/api/v2/order/list/all', data)
            except:
                print("Kryptono获取所有历史数据失败")
                re_get()
            return resp
        resp = re_get()
        # print(resp)
        resp_json = json.loads(resp)
        # if not isinstance(resp_json, list):
        #     # self.logger.error("Kryptono获取所有历史数据失败:[%s]", resp)
        #     return

        return resp_json
        pass

    def get_trade_list(self,symbol,from_id=None,limit=None,recvWindow=None):
        #获取交易清单
        data = {}
        data['symbol'] = symbol
        if not limit is None:
            data['limit'] = limit
        if not from_id is None:
            data['page'] = from_id
        if not recvWindow is None:
            data['recvWindow'] = recvWindow
        else:
            data['recvWindow'] = 5000
        data['timestamp'] = int(time.time()) * 1000
        # print('data:', data)

        def re_get():
            # resp = None
            try:
                global resp
                resp = self.__send("POST", '/api/v2/order/list/trades', data)
            except:
                print("Kryptono获取所有历史数据失败")
                re_get()
            return resp
        resp = re_get()
            # return
        # print('resp',resp)
        resp_json = json.loads(resp)
        # if not isinstance(resp_json, list):
        #     # self.logger.error("Kryptono获取所有历史数据失败:[%s]", resp)
        #     return

        return resp_json
        pass

    def account_information(self,recvWindow=None):
        # 获取账户信息
        data = {}
        if not recvWindow is None:
            data['recvWindow'] = recvWindow
        else:
            data['recvWindow'] = 5000
        data['timestamp'] = int(time.time()) * 1000
        # print('data:', data)

        try:
            resp = self.__send("GET", '/api/v2/account/details', data)
        except:
            # self.logger.error("Kryptono获取所有历史数据失败")
            return
        # print(resp)
        resp_json = json.loads(resp)
        # print(resp_json,'----------------')
        # if not isinstance(resp_json, list):
        #     # self.logger.error("Kryptono获取所有历史数据失败:[%s]", resp)
        #     return

        return resp_json
        pass

    def account_balances(self,recvWindow=None):
        # 获取账户余额
        data = {}
        if not recvWindow is None:
            data['recvWindow'] = recvWindow
        else:
            data['recvWindow'] = 5000
        data['timestamp'] = int(time.time()) * 1000
        # print('data:', data)
        def re_get():
            try:
                global resp
                resp = self.__send("GET", '/api/v2/account/balances', data)
            except:
                # self.logger.error("Kryptono获取所有历史数据失败")
                re_get()
            return resp
        resp = re_get()
            # print('resp',resp,type(resp))
        resp_json = json.loads(resp)
        # if not isinstance(resp_json, list):
        #     # self.logger.error("Kryptono获取所有历史数据失败:[%s]", resp)
        #     return
        # print('resp_json:',resp_json)
        return resp_json
        pass


if __name__ == '__main__':
    # Total must be equal or greater than 0.001 BTC
    kryptono = Kryptono(api_key, secret_key)
    data = {
  "order_symbol" : "SWC_ETH",
  "order_side" : "BUY",
  "order_price" : "0.00020000",
  "order_size" : "500",
  "type" : "LIMIT",
  # "timestamp" : 1507725176599,
  "recvWindow" : 5000
}
    data1 = {
  "symbol" : "SWC_ETH",
        # "order_id":"92fc5c6e-0b99-4c20-a923-952b26fd01ef"
}
    data2 = {
  "order_id" : "4e90694d-7be2-4c15-99d3-71838515281b",
  "order_symbol" : "SWC_ETH"
}
    content = kryptono.cancel_order(**data2)
    # while content is None:
    #     content = kryptono.get_trade_list(**data)
    print(content)
    # print('__main__',pd.DataFrame(content))
    #pd.DataFrame(content)


    # print(kryptono.account_information())