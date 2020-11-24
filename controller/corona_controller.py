import pickle

from constant import constant
import xmltodict
import json
import requests

service_key = constant.SERVICE_KEY
total_service_key = constant.TOTAL_SERVICE_KEY
sido_url = constant.SIDO_URL
total_url = constant.TOTAL_URL


def get_corona_status(region, date):
    if region == "전국":
        region = None

    # 전국 단위 API 호출

    total_request_url = f'{total_url}?ServiceKey={total_service_key}&numOfRows=100'
    if date:
        total_request_url += f'&startCreateDt={date}&endCreateDt={date}'


    total_response = requests.get(total_request_url)
    total_parsed_data = xmltodict.parse(total_response.text)
    total_res_dict = json.loads(json.dumps(total_parsed_data))

    # 전국 더미 만들기

    total_corona = {}
    total_data = {}

    try:
        total_corona = total_res_dict['response']['body']['items']['item']

        if total_res_dict['response']['header']['resultCode'] == '00':
            with open('total_corona.pickle', 'wb') as fw:
                pickle.dump(total_res_dict, fw)
    except:
        with open('total_corona.pickle', 'rb') as fr:
            total_corona = pickle.load(fr)['response']['body']['items']['item']

    total_data = {
        'resutlNegCnt': total_corona['resutlNegCnt'],
        'careCnt': total_corona['careCnt'],
        'accExamCnt': total_corona['accExamCnt'],
    }

    # 시도 단위 API 호출

    sido_request_url = f'{sido_url}?ServiceKey={service_key}&numOfRows=100';
    if date:
        sido_request_url += f'&startCreateDt={date}&endCreateDt={date}'

    sido_response = requests.get(sido_request_url)

    sido_parsed_data = xmltodict.parse(sido_response.text)
    sido_res_dict = json.loads(json.dumps(sido_parsed_data))

    region_data = {}
    corona_list = []
    try:
        corona_list = sido_res_dict['response']['body']['items']['item']

        if sido_res_dict['response']['header']['resultCode'] == '00':
            with open('corona.pickle', 'wb') as fw:
                pickle.dump(sido_res_dict, fw)

    except:
        with open('corona.pickle', 'rb') as fr:
            corona_list = pickle.load(fr)['response']['body']['items']['item']

    is_valid_region = False

    if not region:
        region_data = corona_list[-1]
    else:
        for corona_item in corona_list:
            if corona_item['gubun'] == region:
                region_data = corona_item
                is_valid_region = True
                break
        if not is_valid_region:
            return None

    region_data.update(total_data)

    return region_data
