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

    try:
        corona_list = res_dict['response']['body']['items']['item']

        if region is None:
            return corona_list[-1]

        for corona_item in corona_list:
            if corona_item['gubun'] == region:
                return corona_item
    except:
        return {}

    return None

def get_corona_info(date, region):
    response = requests.get(f'{url}?ServiceKey={service_key}&numOfRows=1000&startCreateDt={date}&endCreateDt={date}')

    parsed_data = xmltodict.parse(response.text)
    res_dict = json.loads(json.dumps(parsed_data))

    try:
        corona_list = res_dict['response']['body']['items']['item']

        if region is None:
            return "다시 말씀해주세요"

        if region == "전국":
            return corona_list[-1]

        for corona_item in corona_list:
            if corona_item['gubun'] == region:
                return corona_item
    except:
        return {}

    return None
