from flask import Flask, request
from controller import corona_controller

app = Flask(__name__)


@app.route('/corona-status')
def hello_world():
    args = request.args.get('region', None)
    data = corona_controller.get_corona_status(args)

    if data is None:

    return data


if __name__ == '__main__':
    app.run()
