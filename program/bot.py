import time
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import random
import logging
from tabulate import tabulate

from program.config import CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET, HANK_ID, LALA_ID
from program.db import Mongo

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# add random response
resp = ['哈哈 真假', '0.0', '7414', '喵喵喵']


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def receive_message(event):    

    # main feature of split money linebot
    # hank and lala only
    if event.source.user_id == LALA_ID or event.source.user_id == HANK_ID:

        if '結算' in event.message.text or '結清' in event.message.text or '算帳' in event.message.text:
            
            pays_more, amount = Mongo.two_sum_difference()
            if pays_more == 'hank':
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Lala 要給 Hank ' + str(amount) + '元!\n帳目已結清'))

            elif pays_more == 'lala':
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Hank 要給 Lala ' + str(amount) + '元!\n帳目已結清'))

            elif pays_more == 'no_one':
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='剛好花一樣錢!! amazing!!'))

            Mongo.clear()
            app.logger.info('Records reset.')
            return

        elif '試算' in event.message.text or '算一下' in event.message.text:

            pays_more, amount = Mongo.two_sum_difference()
            if pays_more == 'hank':
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Lala 現在欠 Hank ' + str(amount) + '元喔!'))

            elif pays_more == 'lala':
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Hank 現在欠 Lala ' + str(amount) + '元喔!'))

            elif pays_more == 'no_one':
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='現在剛好花一樣錢喔!'))
            app.logger.info('Show current amount.')
            return        

        elif '偷看一下' in event.message.text:

            records = Mongo.find_all()
            data = [dict(record) for record in records]

            if data:
                table = tabulate(data, headers="keys", tablefmt="plain", stralign='right')
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='偷看一下! \n-----------------------\n' + table)
                )
                # print(table)
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='現在是空的!')
                )                
            app.logger.info('Ledger screenshot.')
            return

        elif '功能表' in event.message.text or '指令表' in event.message.text:
            line_bot_api.reply_message(
                event.reply_token, 
                TextSendMessage(text='記帳:\nLala or Hank 項目 金額\n----------\n其他功能:\n目前帳目->偷看一下\n試算金額->算一下/試算\n導覽頁面->指令表/功能表')
            )
            app.logger.info('Show menu')
            return       

        elif 'hank' in event.message.text or 'Hank' in event.message.text or 'lala' in event.message.text or 'Lala' in event.message.text: 

            message = event.message.text.split(' ')
            payer = message[0].lower()
            item = message[1]
            amount = message[2]

            if amount.isdigit():

                Mongo.insert_new(payer, item, amount)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=''.join([payer, ' 付了 ', amount, '\n登記好了!'])))
                app.logger.info('New record entered.')

            else:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='格式不對 要重新輸入!'))
            return

        else:

            if event.source.user_id == LALA_ID:
                if '寶寶' in event.message.text:
                    if event.source.type == 'group':
                        id = event.source.group_id
                    else:
                        id = LALA_ID
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
                    return

            num = random.randint(0, len(resp)-1)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=resp[num]))

@app.route('/health-check', methods = ['GET'])
def health_check():
    return 'OK'

if __name__ == "__main__":   
    app.run(debug=True)