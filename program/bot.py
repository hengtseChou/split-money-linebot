import logging
import random
import time

import wcwidth
from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from tabulate import tabulate

from program.config import (
    CHANNEL_ACCESS_TOKEN,
    CHANNEL_SECRET,
    HANK_ID,
    LALA_ID,
)
from program.db import MongoHandler, mongo_handler

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


def calc_difference_in_sum(mongo_handler: MongoHandler):
    sum_values = {"hank": 0, "lala": 0}
    for payer in ["hank", "lala"]:
        pipeline = [{"$group": {"_id": None, "total": {"$sum": "$" + payer}}}]
        result = mongo_handler.records.aggregate(pipeline)
        if result:
            sum_values[payer] += result[0]["total"]

    if sum_values["hank"] > sum_values["lala"]:
        pays_more = "hank"
    elif sum_values["hank"] < sum_values["lala"]:
        pays_more = "lala"
    else:
        pays_more = "no_one"
    return pays_more, abs(sum_values["hank"] - sum_values["lala"])

def send_calc_result_msg(event):
    pays_more, amount = calc_difference_in_sum(mongo_handler)
    if pays_more == "hank":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Lala 現在欠 Hank " + str(amount) + "元喔!"),
        )

    elif pays_more == "lala":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Hank 現在欠 Lala " + str(amount) + "元喔!"),
        )

    elif pays_more == "no_one":
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="現在剛好花一樣錢喔!")
        )


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def receive_message(event: MessageEvent):
    # main feature of split money linebot
    # hank and lala only
    user_id = event.source.user_id

    if not (user_id == LALA_ID or user_id == HANK_ID):
        return
    if any(x in event.message.text for x in ["結算", "結清", "算帳"]):

        send_calc_result_msg(event)
        mongo_handler.clear_all()
        app.logger.info("Records reset.")
        return

    elif any(x in event.message.text for x in ["試算", "算一下"]):
        send_calc_result_msg(event)
        app.logger.info("Show current amount.")
        return

    elif "偷看一下" in event.message.text:
        records = mongo_handler.all_records()
        if records:
            table = tabulate(records, headers="keys", tablefmt="plain", numalign="right")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="偷看一下! \n-----------------------\n" + table),
            )
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="現在是空的!"))
        app.logger.info("Ledger screenshot.")
        return

    elif any(x in event.message.text for x in ["功能表", "指令表"]):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="記帳:\nLala or Hank 項目 金額\n----------\n其他功能:\n目前帳目->偷看一下\n試算金額->算一下/試算\n導覽頁面->指令表/功能表"
            ),
        )
        app.logger.info("Show menu")
        return

    elif any(x in event.message.text for x in ["hank", "Hank", "lala", "Lala"]):
        try:
            message = event.message.text.split(" ")
            payer = message[0].lower()
            amount = message[-1]

            if amount.isdigit() and (payer in ["hank", "lala"]):
                mongo_handler.new_record(payer, amount)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(f"{payer.capitalize()} 付了 {amount}\n登記好了!"),
                )
                app.logger.info("New record entered.")

            else:
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="格式不對 要重新輸入!")
                )
            return

        except Exception as e:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="格式不對 要重新輸入!")
            )
            app.logger.error(str(e))
            return

    if user_id == LALA_ID and "寶寶" in event.message.text:
        line_bot_api.push_message(LALA_ID, TextSendMessage(text="是喔"))
        time.sleep(0.5)
        line_bot_api.push_message(LALA_ID, TextSendMessage(text="澳草喔"))
        time.sleep(0.5)
        line_bot_api.push_message(LALA_ID, TextSendMessage(text="愛你喔"))
        time.sleep(0.5)
        line_bot_api.push_message(LALA_ID, TextSendMessage(text="寶寶"))
        return

    resp = ["哈哈 真假", "0.0", "7414", "喵喵喵"]
    num = random.randint(0, len(resp) - 1)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=resp[num]))
    return


@app.route("/health-check", methods=["GET"])
def health_check():
    return "OK"


if __name__ == "__main__":
    app.run(debug=True)
