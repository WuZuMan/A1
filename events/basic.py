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
        package_id='11539',
        sticker_id='52114130'
    )
    line_bot_api.reply_message(
        event.reply_token, 
        [text_message, sticker_message])