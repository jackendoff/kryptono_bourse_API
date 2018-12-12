import requests
import json
'''
请求url，获取数据，返回数据类型
'''


def get_data(url,**kwargs):
    if kwargs:
        print('11111')
        data_re = requests.get(url, headers=kwargs)
        data = json.loads(data_re.content.decode())
        return data

    # print(kwargs)
    else:
        data_re = requests.get(url)
        data = json.loads(data_re.content.decode())
        return data

def post_data(url,**kwargs):
    pass


if __name__ == '__main__':
    url = 'https://api.fcoin.com/v2/market/depth/full/dageth'
    data = get_data(url)
    print(data,type(data))