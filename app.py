from flask import Flask, request
from controller import corona_controller, news_controller

app = Flask(__name__)


@app.route('/corona-status')
def corona_status():
    args = request.args.get('region', None)
    data = corona_controller.get_corona_status(args)

    if data is None:
        return {'message': '검증 오류'}, 400

    return data


@app.route('/news')
def corona_news():
    data = news_controller.get_news()

    return data


if __name__ == '__main__':
    app.run()
