from requests_data import get_data


class AccountApi(object):
    '''
    账户api调用
    '''
    def __init__(self):
        self.account_url_base = 'https：//p.kryptono.exchange/k'

        pass

    def new_order(self):
        pass





if __name__ == '__main__':
    pub_api = AccountApi()
    symbol = 'KNOW_ETH'
    print(pub_api.order_book(symbol))