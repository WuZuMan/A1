from line_bot_api import *
from events.basic import *

def about_us_event(event):
    emoji =[
        {
            "index":0,
            "productId":"5ac21c4e031a6752fb806d5b",
            "emojiId":"005"

        },
        {
            "index":17,
            "productId":"5ac21c4e031a6752fb806d5b",
            "emojiId":"002"
        }
    ]
    text_message=TextSendMessage(text='''$ Master Finance $
Hello 您好歡迎您成為hihi的朋友
我是財經好幫手
-這裡有股票匯率資訊
-直接點選下方press it 選單功能                                                                     
-Weclome~''',emojis=emoji)
    
    sticker_message = StickerSendMessage(
        package_id='11537',
        sticker_id='52002739'
    )



    buttons_template = TemplateSendMessage(
        alt_text="小幫手 template",
        template=ButtonsTemplate(
            title="選擇服務",
            text="請選擇",
            thumbnail_image_url="https://i.imgur.com/aYbxhvj.jpeg",
            actions=[
                MessageTemplateAction(
                    label="油價查詢",
                    text="油價查詢"
                ),
                 MessageTemplateAction(
                     label="匯率查詢",
                      text="匯率查詢"
                ),
                 MessageTemplateAction(
                     label="股價查詢",
                     text="股價查詢"
                )
            ]            
        )
    )

    line_bot_api.reply_message(
        event.reply_token, 
        [text_message, sticker_message])
    
def push_msg(event,msg):
    try:
        user_id = event.source.user_id
        line_bot_api.push_message(user_id,TextSendMessage(text=msg))
    except:
        room_id = event.source.room_id
        line_bot_api.push_message(room_id,TextSendMessage(text=msg))
        


def Usage(event):
    push_msg(event,"🛡🛡查詢方法🛡🛡\
            \n \
            \n 🎈小幫手可以查詢油價👉匯率👉股價\
            \n \
            \n 🎁油價通知 👉👉👉 輸入查詢油價\
            \n 🎁匯率通知 👉👉👉 輸入查詢匯率\
            \n 🎁匯率兌換 👉👉👉 換匯USD/TWD\
            \n 🎁股價查詢 👉👉👉 輸入#股票代號\
            ")