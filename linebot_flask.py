from __future__ import unicode_literals
import os
import pandas as pd
from datetime import datetime
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from drive_method import drive_method

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

        if 'hank' in event.message.text or 'Hank' in event.message.text:
            message = event.message.text
            amount = message.split(' ')[-1]

            drive = drive_method()
            drive.download('ledger.csv', config.get('drive-api', 'file_id')) 

            df = pd.read_csv('ledger.csv')
            new_row = pd.Series({'date': datetime.now().strftime("%Y/%m/%d, %H:%M"), 'hank': amount, 'lala': 0})
            df = pd.concat([df, new_row.to_frame().T], ignore_index=True)
            df.to_csv('ledger.csv', index=False)

            drive.update('ledger.csv', config.get('drive-api', 'file_id'))

            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Hank 付了 ' + str(amount) + '\n登記好了!'))

        elif 'lala' in event.message.text or 'Lala' in event.message.text:
            message = event.message.text
            amount = message.split(' ')[-1]

            drive = drive_method()
            drive.download('ledger.csv', config.get('drive-api', 'file_id')) 
            
            df = pd.read_csv('ledger.csv')
            new_row = pd.Series({'date': datetime.now().strftime("%Y/%m/%d, %H:%M"), 'hank': 0, 'lala': amount})
            df = pd.concat([df, new_row.to_frame().T], ignore_index=True)
            df.to_csv('ledger.csv', index=False)

            drive.update('ledger.csv', config.get('drive-api', 'file_id'))

            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Lala 付了 ' + str(amount) + '\n登記好了!'))

        elif '結算' in event.message.text or '結清' in event.message.text or '算帳' in event.message.text:

            drive = drive_method()
            drive.download('ledger.csv', config.get('drive-api', 'file_id')) 
            
            df = pd.read_csv('ledger.csv')

            hank_minus_lala = df.hank.sum() - df.lala.sum()

            if hank_minus_lala > 0:

                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Lala 要給 Hank ' + str(hank_minus_lala) + '元!\n帳目已結清'))

            elif hank_minus_lala < 0:

                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Hank 要給 Lala ' + str(hank_minus_lala*-1) + '元!\n帳目已結清'))

            elif hank_minus_lala == 0:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='剛好花一樣錢!! amazing!!'))

            df = df[0:0]
            df.to_csv('ledger.csv', index=False)
            drive.update('ledger.csv', config.get('drive-api', 'file_id'))





if __name__ == "__main__":
    app.run(debug=True)