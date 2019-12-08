from queue import Queue
from threading import Thread

from flask import Flask, request
from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel, PeerChat, PeerUser

import config


class Item:
    chat = ''
    text = ''
    chattype = ''
    delete = 0


def queue_putter():
    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def root():
        item = Item()
        item.chat = request.form['chat']
        item.text = request.form['text']
        item.chattype = request.form.get('chattype', '')
        item.delete = int(request.form.get('delete', 0))

        q.put(item)
        return 'OK!'

    app.run(host="0.0.0.0", debug=False, port=8080)


q = Queue()
t = Thread(target=queue_putter)
t.daemon = True
t.start()

tg = TelegramClient(StringSession(config.session), config.api_id, config.api_hash)
tg.start()

while True:
    item = q.get()
    if item is None:
        break
    try:
        if item.chattype == 'channel':
            entity = tg.get_entity(PeerChannel(int(item.chat)))
        elif item.chattype == 'user':
            entity = tg.get_entity(PeerUser(int(item.chat)))
        elif item.chattype == 'chat':
            entity = tg.get_entity(PeerChat(int(item.chat)))
        else:
            entity = item.chat
        msg = tg.send_message(entity, item.text)
        if item.delete:
            msg.delete()
    except ValueError as e:
        print(e.args)

    q.task_done()
