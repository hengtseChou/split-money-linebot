from __future__ import unicode_literals
import os
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


app = Flask(__name__)

import configparser

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def receive_message_and_edit_file(event):
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        if 'hank' or 'Hank' in event.message.text:
            message = event.message.text
            amount = message.split(' ')[-1]


            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='登記好了!'))
        elif 'lala' or 'Lala' in event.message:
            message = event.message.text
            amount = message.split(' ')[-1]


            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='登記好了!'))




if __name__ == "__main__":
    app.run(debug=True)