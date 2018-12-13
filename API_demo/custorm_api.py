# coding=utf-8
from content import api_key, secret_key
import hashlib
import hmac
import http.client as http
import json
import logging
import time
import urllib


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
        data['symbol'] = order_symbol
        data['order_side'] = order_side
        data['order_price'] = order_price
        data['order_size'] = order_size
        data['type'] = type
        if not stop_price is None: data['stop_price'] = stop_price
        if not recvWindow is None: data['recvWindow'] = recvWindow
        else:data['recvWindow'] = 5000
        data['timestamp'] = int(time.time()) * 1000
        # print(data)

        try:
            resp = self.__send("POST", '/api/v2/order/test', data)
        except:
            # self.logger.error("Kryptono获取所有历史数据失败")
            return
        print(resp)
        resp_json = json.loads(resp)
        if not isinstance(resp_json, list):
            # self.logger.error("Kryptono获取所有历史数据失败:[%s]", resp)
            return

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

        try:
            resp = self.__send("DELETE", '/api/v2/order/cancel', data)
        except:
            # self.logger.error("Kryptono获取所有历史数据失败")
            return
        print(resp)
        resp_json = json.loads(resp)
        if not isinstance(resp_json, list):
            # self.logger.error("Kryptono获取所有历史数据失败:[%s]", resp)
            return

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

    def order_detail(self,order_id,recvWindow):
        '''
        获取订单明细
        :param order_id:
        :param recvWindow:
        :return:
        '''
        data = {}
        data['order_id'] = order_id
        data['type'] = type
        if not recvWindow is None:
            data['recvWindow'] = recvWindow
        else:
            data['recvWindow'] = 5000
        data['timestamp'] = int(time.time()) * 1000
        print('data:',data)

        try:
            resp = self.__send("POST", '/api/v2/order/details', data)
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
        print('data:', data)

        try:
            resp = self.__send("POST", '/api/v2/order/list/open', data)
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
        print('data:', data)

        try:
            resp = self.__send("POST", '/api/v2/order/list/completed', data)
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
        print('data:', data)

        try:
            resp = self.__send("POST", '/api/v2/order/list/all', data)
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
        print('data:', data)

        try:
            resp = self.__send("POST", '/api/v2/order/list/trades', data)
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

    def account_information(self,recvWindow=None):
        # 获取账户信息
        data = {}
        if not recvWindow is None:
            data['recvWindow'] = recvWindow
        else:
            data['recvWindow'] = 5000
        data['timestamp'] = int(time.time()) * 1000
        print('data:', data)

        try:
            resp = self.__send("GET", '/api/v2/account/details', data)
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

    def account_balances(self,recvWindow=None):
        # 获取账户余额
        data = {}
        if not recvWindow is None:
            data['recvWindow'] = recvWindow
        else:
            data['recvWindow'] = 5000
        data['timestamp'] = int(time.time()) * 1000
        print('data:', data)

        try:
            resp = self.__send("GET", '/api/v2/account/balances', data)
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


if __name__ == '__main__':
    kryptono = Kryptono(api_key, secret_key)
    data = {
  "limit" : 10,
  "page" : 0,
  "symbol" : "KNOW_BTC",
  "timestamp" : 1429514463299,
  "recvWindow" : 5000
}
    print(kryptono.account_balances())