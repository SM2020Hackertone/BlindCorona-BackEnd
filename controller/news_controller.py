from multiprocessing import Pool

import requests

from constant import constant
from fake_useragent import UserAgent
from selenium import webdriver

driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.implicitly_wait(1)

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
    naver_news_list = list(filter(lambda x: 'https://news.naver.com' in x['link'] and 'sports' not in x['originallink'],
                                  news_list))[:10]

    return {
        'news': naver_news_list,
    }


def _get_img(news):
    driver.get(news['link'])

    try:
        photo_element = driver.find_element_by_class_name('end_photo_org')
        img_element = photo_element.find_element_by_tag_name('img')
        img_src = img_element.get_attribute('src')
        news['img'] = img_src
    except:
        return


def get_img_api(link):
    driver.get(link)

    try:
        photo_element = driver.find_element_by_class_name('end_photo_org')
        img_element = photo_element.find_element_by_tag_name('img')
        img_src = img_element.get_attribute('src')
        return img_src
    except:
        return


def get_single_news(link):
    driver.get(link)

    news = {}

    photo_element = driver.find_element_by_class_name('end_photo_org')
    img_element = photo_element.find_element_by_tag_name('img')
    img_src = img_element.get_attribute('src')
    news['img'] = img_src
    news['title'] = driver.find_element_by_id('articleTitle').text
    news['content'] = driver.find_element_by_id('articleBodyContents').text
    news['date'] = driver.find_element_by_class_name('t11').text

    return news
