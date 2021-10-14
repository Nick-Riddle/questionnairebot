import os

import flask
from telebot import types

from bot import bot
from config import TOKEN, APP_NAME

server = flask.Flask(__name__)


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(
        flask.request.stream.read().decode('utf-8'))])
    return '!', 200


@server.route('/', methods=['GET'])
def index():
    bot.remove_webhook()
    bot.set_webhook(url=f'https://{APP_NAME}.herokuapp.com/{TOKEN}')
    return 'Hello from Heroku!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
