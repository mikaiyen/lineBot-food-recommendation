
from flask import Flask
app = Flask(__name__)

import json
#import flask
from flask import Flask, request, abort
from linebot import  LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    PostbackEvent,
    PostbackTemplateAction
)
from linebot.models import *


import random

# from foodGPT
from openai import OpenAI
import re

client = OpenAI(
                    # defaults to os.environ.get("OPENAI_API_KEY")
                    api_key="", # yor api key
                )


def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
# from foodGPT

# Channel access token
line_bot_api = LineBotApi('')
# Channel secret
handler = WebhookParser('')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    #獲得使用者輸入的訊息
    body = request.get_data(as_text=True)
    try:
        #送出訊息
        events =handler.parse(body, signature)
        print(handler)
    except InvalidSignatureError:
        #送出Bad request (400)
        abort(400)

    for event in events:

        if isinstance(event, MessageEvent):  # 如果有訊息事件
            if event.message.text == "@吃啥":
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TemplateSendMessage(
                        alt_text='Buttons template',
                        template=ButtonsTemplate(
                            title='step1',
                            text='用餐時間',
                            actions=[
                                PostbackTemplateAction(
                                    label='早餐',
                                    text='早餐',
                                    data='A&早餐'
                                ),
                                PostbackTemplateAction(
                                    label='午餐',
                                    text='午餐',
                                    data='A&午餐'
                                ),
                                PostbackTemplateAction(
                                    label='晚餐',
                                    text='晚餐',
                                    data='A&晚餐'
                                ),
                                PostbackTemplateAction(
                                    label='點心',
                                    text='點心',
                                    data='A&點心'
                                )
                            ]
                        )
                    )
                )
        elif isinstance(event, PostbackEvent):  # 如果有回傳值事件

            if event.postback.data[0:1] == "A":  # 如果回傳值為「體感冷暖」

                tem = event.postback.data[2:]  # 透過切割字串取得溫度文字

                line_bot_api.reply_message(   # 回復「飯或麵或其他」按鈕樣板訊息
                    event.reply_token,
                    TemplateSendMessage(
                        alt_text='Buttons template',
                        template=ButtonsTemplate(
                            title='step2',
                            text='請選擇美食類別',
                            actions=[
                                PostbackTemplateAction(  # 將第一步驟選擇的地區，包含在第二步驟的資料中
                                    label='飯',
                                    text='飯',
                                    data='B&' + tem + '&飯'
                                ),
                                PostbackTemplateAction(
                                    label='麵',
                                    text='麵',
                                    data='B&' + tem + '&麵'
                                ),
                                PostbackTemplateAction(
                                    label='其他',
                                    text='其他',
                                    data='B&' + tem + '&其他'
                                )
                            ]
                        )
                    )
                )
            elif event.postback.data[0:1] == "B":

                result = event.postback.data[2:].split('&')  # 回傳值的字串切割

                line_bot_api.reply_message(
                    event.reply_token,
                    TemplateSendMessage(
                        alt_text='Buttons template',
                        template=ButtonsTemplate(
                            title='step3',
                            text='預算範圍',
                            actions=[
                                PostbackTemplateAction(
                                    label='無限制',
                                    text='無限制',
                                    data='C&' + result[0] + '&' + result[1] + '&無限制'
                                ),
                                PostbackTemplateAction(
                                    label='500-1000元',
                                    text='500-1000元',
                                    data='C&' + result[0] + '&' + result[1] + '&500-1000元'
                                ),
                                PostbackTemplateAction(
                                    label='200-500元',
                                    text='200-500元',
                                    data='C&' + result[0] + '&' + result[1] + '&200-500元'
                                ),
                                PostbackTemplateAction(
                                    label='200元以內',
                                    text='200元以內',
                                    data='C&' + result[0] + '&' + result[1] + '&200元以內'
                                )
                            ]
                        )
                    )
                )
            elif event.postback.data[0:1] == "C":

                result = event.postback.data[2:].split('&')  # 回傳值的字串切割

                line_bot_api.reply_message(
                    event.reply_token,
                    TemplateSendMessage(
                        alt_text='Buttons template',
                        template=ButtonsTemplate(
                            title='step4',
                            text='能接受的辣度',
                            actions=[
                                PostbackTemplateAction(
                                    label='大辣',
                                    text='大辣',
                                    data='D&' + result[0] + '&' + result[1] + '&' + result[2] + '&大辣'
                                ),
                                PostbackTemplateAction(
                                    label='中辣',
                                    text='中辣',
                                    data='D&' + result[0] + '&' + result[1] + '&' + result[2] + '&中辣'
                                ),
                                PostbackTemplateAction(
                                    label='小辣',
                                    text='小辣',
                                    data='D&' + result[0] + '&' + result[1] + '&' + result[2]  + '&小辣'
                                ),
                                PostbackTemplateAction(
                                    label='不辣',
                                    text='不辣',
                                    data='D&' + result[0] + '&' + result[1] + '&' + result[2] + '&不辣'
                                )
                            ]
                        )
                    )
                )
            elif event.postback.data[0:1] == "D":

                result = event.postback.data[2:].split('&')  # 回傳值的字串切割

                line_bot_api.reply_message(
                    event.reply_token,
                    TemplateSendMessage(
                        alt_text='Buttons template',
                        template=ButtonsTemplate(
                            title='step5',
                            text='體感冷暖',
                            actions=[
                                PostbackTemplateAction(
                                    label='冷',
                                    text='冷',
                                    data='E&' + result[0] + '&' + result[1] + '&' + result[2] + '&' + result[3] + '&冷'
                                ),
                                PostbackTemplateAction(
                                    label='暖',
                                    text='暖',
                                    data='E&' + result[0] + '&' + result[1] + '&' + result[2] + '&' + result[3] + '&暖'
                                ),
                                PostbackTemplateAction(
                                    label='適中',
                                    text='適中',
                                    data='E&' + result[0] + '&' + result[1] + '&' + result[2] + '&' + result[3] + '&適中'
                                )
                            ]
                        )
                    )
                )
            elif event.postback.data[0:1] == "E":

                result = event.postback.data[2:].split('&')  # 回傳值的字串切割

                temperature = result[4]
                staple = result[1]
                spice = result[3]
                meal = result[0]
                budget = result[2]
                prompt = f"I feel {temperature}. I prefer {staple} and {spice} I want to have {meal}. The budget is {budget}. Please recommend me a food according to my situation. Describe three reasons you recommend this food. Answer the answer with following pattern: I remmand ~\nHere's why:\nthe reason"
                answer = chat_gpt(prompt)
                # from foodGPT
                answerstr = str(answer)
                print(answerstr)
                
                message=TextSendMessage(text=answerstr)
                line_bot_api.reply_message(event.reply_token,message)


    #回覆OK
    return 'OK'



if __name__ == '__main__':
    app.run(port=5000)


    #執行.py和ngrok.exe後cmd輸入 ngrok http 5000 ，複製 Forwarding網址/callback 到 Messaging API 的 Webhook URL選擇use即上線