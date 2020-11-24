import pickle

from constant import constant
import xmltodict
import json
import requests

service_key = constant.SERVICE_KEY
url = constant.URL


def get_corona_status(region):
    response = requests.get(f'{url}?ServiceKey={service_key}&numOfRows=1000')

    parsed_data = xmltodict.parse(response.text)
    res_dict = json.loads(json.dumps(parsed_data))

    with open('corona.pickle', 'wb') as fw:
        pickle.dump(res_dict, fw)

    try:
        raise Exception('오류')
        corona_list = res_dict['response']['body']['items']['item']

        if region is None:
            return corona_list[-1]

        for corona_item in corona_list:
            if corona_item['gubun'] == region:
                return corona_item
    except:
        with open('corona.pickle', 'rb') as fr:
            res_dict = pickle.load(fr)
            corona_list = res_dict['response']['body']['items']['item']

            if region is None:
                return corona_list[-1]

            for corona_item in corona_list:
                if corona_item['gubun'] == region:
                    return corona_item

    return None
