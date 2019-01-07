import logging
# from logging.handlers import RotatingFileHandler

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello world!"


if __name__ == '__main__':
    # handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    # handler.setLevel(logging.INFO)
    # app.logger.addHandler(handler)
    app.logger.basicConfig(filename='error.log', level=logging.DEBUG)
    app.logger.info('Started')
    app.run()


