from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# LINE 聊天機器人的基本資料
line_bot_api = LineBotApi('P11lhTsFnl1OLyiEjOdEMbdVY6vpAnRs3dv0BR9Tmr7NaoWtfHyjEtrzWQaue5FzVEqAL5pGyG/p7WPrVA6tD+Huc58H99/HjJ5wkgcq6umBmQu7Hy/YIaixDNrJxIOs9wvq3a+wF0YmU8jpqLk7aQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f03510c3f568b30cf87149b2654fcf2f')

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

# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

if __name__ == "__main__":
    app.run()