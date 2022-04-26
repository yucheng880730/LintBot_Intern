import os
import re
import json
import scraper as x
from dotenv import load_dotenv
from flask import Flask, request, abort
load_dotenv()

ChannelAccessToken = os.getenv('ChannelAccessToken')
ChannelSecret = os.getenv('ChannelSecret')
UserID = os.getenv('UserID')

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(ChannelAccessToken)
# Channel Secret
handler = WebhookHandler(ChannelSecret)

start_message = FlexSendMessage(
    alt_text='Hi, 我是林祐丞 Leo',
    contents={
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "小提示!!",
                "weight": "bold",
                "size": "xxl",
                "margin": "md"
            },
            {
                "type": "text",
                "text": "Line Bot 機器人小提示~",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True
            },
            {
                "type": "text",
                "text": "試著輸入下列提示吧!",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True
            },
            {
                "type": "separator",
                "margin": "xxl"
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "xxl",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "\"開始\"",
                        "size": "sm",
                        "color": "#555555",
                        "flex": 0
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "\"介紹\"",
                        "size": "sm",
                        "color": "#555555",
                        "flex": 0
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                    {
                        "type": "text",
                        "text": "\"更多\"",
                        "size": "sm",
                        "color": "#555555",
                        "flex": 0
                    }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "xxl",
                    "contents": [
                    {
                        "type": "text",
                        "text": "肚子好\"餓\"",
                        "size": "sm",
                        "color": "#555555"
                    }
                    ]
                }
                ]
            }
            ]
        },
        "styles": {
            "footer": {
            "separator": True
            }
        }
        }
    )

line_bot_api.push_message(UserID, start_message)

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text

    if re.match('掰掰',message):
        # byeMessage = [
        #     {
        #         "type": "text",
        #         "text": "掰掰~",
        #     }, 
        #     {
        #         "type": "sticker",
        #         "package_id": "11538",
        #         "sticker_id": "51626533"  
        #     }   
        # ]
        line_bot_api.push_message(UserID, TextSendMessage(text='掰掰~'))
        sticker_message = StickerSendMessage(
            package_id='11538',
            sticker_id='51626533'
        )
        line_bot_api.reply_message(event.reply_token, sticker_message)

    elif re.search('謝謝', message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage("不客氣，下次再聊天哦!"))

    elif re.search('開始', message):
        introduce_message = "我是林祐丞"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(introduce_message))

    elif re.search('介紹', message):
        flex_message = FlexSendMessage(
            alt_text='Leo簡介',
            contents={
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "action": {
                    "type": "uri",
                    "uri": "https://linecorp.com"
                    },
                    "url": "https://gateway.pinata.cloud/ipfs/QmYvhuZybeyX1Q8PQhFkFg3wu8n8YSb1Q5mLnE87GeWugg"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "action": {
                    "type": "uri",
                    "uri": "https://linecorp.com"
                    },
                    "contents": [
                    {
                        "type": "text",
                        "text": "Yucheng Lin",
                        "size": "xl",
                        "weight": "bold"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                            {
                                "type": "text",
                                "text": "國立政治大學",
                                "weight": "bold",
                                "margin": "sm",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": "資管碩士班",
                                "size": "sm",
                                "align": "end",
                                "color": "#aaaaaa"
                            }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                            {
                                "type": "text",
                                "text": "國立中正大學",
                                "weight": "bold",
                                "margin": "sm",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": "資管學士班",
                                "size": "sm",
                                "align": "end",
                                "color": "#aaaaaa"
                            }
                            ]
                        }
                        ]
                    },
                    {
                        "type": "text",
                        "wrap": True,
                        "color": "#17202A",
                        "size": "md",
                        "text": "Junior Web Developer / Blockchain Engineer Specialized in front end development and developing DApp. I am a lively and outgoing person. My strength is good communication skills and having lots of teamwork experience. "
                    },
                    {
                        "type": "text",
                        "text": "輸入: 想了解更多!!",
                        "wrap": True,
                        "color": "#aaaaaa",
                        "size": "sm"
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "margin": "xxl",
                        "action": {
                        "type": "uri",
                        "label": "View Personal Web",
                        "uri": "https://yuchengleoweb.herokuapp.com/"
                        },
                        "color": "#5DADE2"
                    }
                    ]
                }
            }
        )
        line_bot_api.reply_message(event.reply_token, flex_message)

    elif re.search('更多', message):
        personal_template_message = TemplateSendMessage(
            alt_text='更多內容',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg',
                        title='技術相關',
                        text='Java, Python, JavaScript, React, Solidity, K8s, Docker, AWS',
                        actions=[
                            URIAction(
                                label='馬上查看',
                                uri='https://github.com/yucheng880730'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/8/80/LinkedIn_Logo_2013.svg',
                        title='Linkedin',
                        text='了解更多: CV、證照、個人網頁',
                        actions=[
                            URIAction(
                                label='馬上查看',
                                uri='https://www.linkedin.com/in/yucheng-lin0730/'
                            ) 
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/b/b1/Medium_logo_Wordmark_Black.svg',
                        title='Medium',
                        text='文章撰寫',
                        actions=[
                            URIAction(
                                label='馬上查看',
                                uri='https://medium.com/@yucheng2k13'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, personal_template_message)

    elif re.search('餓',message):
        flex_message = TextSendMessage(text='你在哪一個縣市呢',
                               quick_reply=QuickReply(items=[
                                   QuickReplyButton(action=MessageAction(label="台北市", text="台北市")),
                                   QuickReplyButton(action=MessageAction(label="台中市", text="台中市")),
                                   QuickReplyButton(action=MessageAction(label="高雄市", text="高雄市")),
                                   QuickReplyButton(action=MessageAction(label="台南市", text="台南市")),
                                   QuickReplyButton(action=MessageAction(label="桃園市", text="桃園市")),
                                   QuickReplyButton(action=MessageAction(label="新北市", text="新北市")),
                                   QuickReplyButton(action=MessageAction(label="嘉義縣", text="嘉義縣")),
                                   QuickReplyButton(action=MessageAction(label="台東縣", text="台東縣")),
                                   QuickReplyButton(action=MessageAction(label="花蓮縣", text="花蓮縣")),
                                   QuickReplyButton(action=MessageAction(label="宜蘭縣", text="宜蘭縣"))
                               ]))
        line_bot_api.reply_message(event.reply_token, flex_message)

    elif re.search('台北', message):
        food = x.scrape("台北市")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(food))

    elif re.search('台中', message):
        food = x.scrape("台中市")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(food))

    elif re.search('高雄', message):
        food = x.scrape("高雄市")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(food))

    elif re.search('台南', message):
        food = x.scrape("台南市")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(food))

    elif re.search('桃園', message):
        food = x.scrape("桃園市")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(food))

    elif re.search('新北', message):
        food = x.scrape("新北市")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(food))

    elif re.search('嘉義', message):
        food = x.scrape("嘉義縣")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(food))

    elif re.search('台東', message):
        food = x.scrape("台東縣")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(food))

    elif re.search('花蓮', message):
        food = x.scrape("花蓮縣")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(food))
    elif re.search('宜蘭', message):
        food = x.scrape("宜蘭")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(food))

    # 沒有比對重複回話
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
        

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)