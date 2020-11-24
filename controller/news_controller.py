import requests

from constant import constant
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver

naver_url = constant.NAVER_URL
client_id = constant.CLIENT_ID
client_secret = constant.CLIENT_SECRET


def get_news():
    ua = UserAgent()

    response = requests.get(naver_url,
                            headers={
                                'X-Naver-Client-Id': client_id,
                                'X-Naver-Client-Secret': client_secret,
                                'User-Agent': ua.random
                            },
                            params={
                                'query': '코로나19',
                                'start': 1,
                                'display': 100
                            })

    news_list = response.json()['items']
    naver_news_list = list(filter(lambda x: 'news.naver.com' in x['link'], news_list))

    # for news in naver_news_list:
    #     news_response = requests.get(news['link'])
    #     html = news_response.text
    #     soup = BeautifulSoup(html, 'html.parser')
    #     img = soup.select('#articleBodyContents > span.end_photo_org > img')
    #     print(img)

    news_response = requests.get(naver_news_list[0]['link'])
    print(news_response)
    html = news_response.text
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.select('.end_photo_org')
    print(img)

    return {
        'news': naver_news_list,
    }
