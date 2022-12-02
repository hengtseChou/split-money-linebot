import os
import time
import configparser
import pandas as pd
from datetime import datetime
from flask import Flask, request, abort, Response

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import urllib
from drive_method import drive_method, new_entry

app = Flask(__name__)



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

    # main feature of split money linebot
    # hank and lala only
    if event.source.user_id == "U0e99829e94c36b375cdd8ecce89e7364" or event.source.user_id == "U3288aae77c04c706f1e72cf8e7f1fff5":

        if 'hank' in event.message.text or 'Hank' in event.message.text:
            message = event.message.text
            amount = message.split(' ')[-1]

            if amount.isdigit():
                drive = drive_method('ledger.csv', config.get('drive-api', 'file_id'))
                new_entry(drive, 'hank', amount)

                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Hank 付了 ' + str(amount) + '\n登記好了!'))
                print('ran new entry.')
            else:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='格式不對 要重新輸入!'))


        elif 'lala' in event.message.text or 'Lala' in event.message.text:
            message = event.message.text
            amount = message.split(' ')[-1]

            if amount.isdigit():
                drive = drive_method('ledger.csv', config.get('drive-api', 'file_id'))
                new_entry(drive, 'lala', amount)

                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Lala 付了 ' + str(amount) + '\n登記好了!'))
                print('ran new entry.')
            else:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='格式不對 要重新輸入!'))


        elif '結算' in event.message.text or '結清' in event.message.text or '算帳' in event.message.text:

            drive = drive_method('ledger.csv', config.get('drive-api', 'file_id'))
            drive.download()            
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
            drive.upload()
            print('ledger settled')

        elif '偷看一下' in event.message.text:
            drive = drive_method('ledger.csv', config.get('drive-api', 'file_id'))
            drive.download()
            df = pd.read_csv('ledger.csv')
            if df.empty:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='現在是空的!'))
            else:
                text = df.to_string(index=False)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='偷看一下! \n----------------\n' + text))
            print('take a look of the ledger')

        elif '功能表' in event.message.text or '指令表' in event.message.text:
            line_bot_api.reply_message(
                event.reply_token, 
                TextSendMessage(text='記帳:\nLala or Hank 空一格 金額\n----------\n其他功能:\n目前帳目->偷看一下\n試算金額->算一下/試算\n導覽頁面->指令表/功能表')
            )
            print('shown menu')

        elif '試算' in event.message.text or '算一下' in event.message.text:

            drive = drive_method('ledger.csv', config.get('drive-api', 'file_id'))
            drive.download()            
            df = pd.read_csv('ledger.csv')

            hank_minus_lala = df.hank.sum() - df.lala.sum()

            if hank_minus_lala > 0:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Lala 現在欠 Hank ' + str(hank_minus_lala) + '元喔!'))

            elif hank_minus_lala < 0:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Hank 現在欠 Lala ' + str(hank_minus_lala*-1) + '元喔!'))

            elif hank_minus_lala == 0:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='現在剛好花一樣錢喔!'))
            print('show current amount')

    if event.source.user_id == "U0e99829e94c36b375cdd8ecce89e7364":
        if '寶寶' in event.message.text:
            if event.source.type == 'group':
                id = event.source.group_id
            else:
                id = 'U0e99829e94c36b375cdd8ecce89e7364'
            line_bot_api.push_message(
            id,
            TextSendMessage(text='是喔'))
            time.sleep(0.5)
            line_bot_api.push_message(
            id,
            TextSendMessage(text='澳草喔'))
            time.sleep(0.5)
            line_bot_api.push_message(
            id,
            TextSendMessage(text='愛你喔'))
            time.sleep(0.5)
            line_bot_api.push_message(
            id,
            TextSendMessage(text='寶寶'))   

# use scheduler to wake up app at daytime
# every 15 mins on 8pm-3am, taipei time

def wake():
    print('wake up! called by cron-job.org')

@app.route('/', methods=['GET', 'POST'])
def wake_server():
    try:
        result = wake()
    except Exception as e:
        return Response('Error: {}'.format(str(e)), status=500)
    return Response(result, status=200)

if __name__ == "__main__":   
    app.run(debug=True)