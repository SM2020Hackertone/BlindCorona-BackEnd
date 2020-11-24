from flask import Flask, request
from controller import corona_controller, news_controller
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


@app.route('/corona-status')
def corona_status():
    args = request.args.get('region', None)
    data = corona_controller.get_corona_status('전국', '20201123')

    if data is None:
        return {'message': '검증 오류'}, 400

    return data


@app.route('/corona-info')
def corona_info():
    args = request.args.get('text', None)
    if args is None:
        return {'message': '음성 메세지를 입력해주세요'}, 400
    language_processing_server = "http://172.30.1.58:3000/analyze"
    parameter = {'text': args}
    r = requests.get(language_processing_server, parameter)
    date = r.json()['Date']
    region = r.json()['Location']

    data = corona_controller.get_corona_status(region, date)

    return {'data': data}, 200


@app.route('/news')
def corona_news():
    data = news_controller.get_news()
    return data


@app.route('/news/img', methods=['POST'])
def corona_news_img():
    args = request.get_json(force=True)
    print(args)
    data = news_controller.get_img_api(args['link'])

    return {
        'img': data,
    }


@app.route('/news', methods=['POST'])
def corona_detail():
    args = request.get_json(force=True)
    data = news_controller.get_single_news(args['link'])

    return {
        'news': data
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
