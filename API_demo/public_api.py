from requests_data import get_data


class PublicApi(object):
    '''
    公共api调用
    '''
    #####################一般api
    def __init__(self):
        self.common_url_base = 'https://p.kryptono.exchange/k/'
        self.market_url_base = 'https://engine2.kryptono.exchange/'
        pass

    def text(self):
        '''测试与Rest API的连接'''
        url = self.common_url_base+'api/v2/ping'
        data = get_data(url)
        return data

    def server_time(self):
        '''测试与Rest API的连接并获取当前服务器时间'''
        url = self.common_url_base+'api/v2/time'
        return get_data(url)
        pass

    def trans_data(self):
        '''当前的交易所交易规则和符号信息'''
        url = self.common_url_base+'api/v2/exchange-info'
        return get_data(url)

    def mark_price(self):
        ''''''
        url = self.common_url_base+'api/v2/market-price'
        return get_data(url)

    ########################市场数据api
    def trade_history(self,symbol):
        '''获取特定符号的交易历史记录'''
        # print(symbol,type(symbol))
        url = self.market_url_base+'api/v1/ht?symbol='+symbol
        return get_data(url)

    def order_book(self,symbol):
        '''获取当前订单簿数据'''
        url = self.market_url_base+'api/v1/dp?symbol='+symbol
        return get_data(url)


if __name__ == '__main__':
    pub_api = PublicApi()
    symbol = 'KNOW_ETH'
    print(pub_api.trade_history(symbol))