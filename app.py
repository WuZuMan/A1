#載入linebot 所需的套件
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler, exceptions)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *        #* means all

app=Flask(__name__)
# paste your "Channel Access Token"
line_bot_api = LineBotApi('Hr4OfRuaES7MBwy/6a2FC3tDKTQrfzgutDKQ1gXaZ5qwkIyb9TbGlk2xgNbMNzIjmewn6u9nX8pn5hwWul7HED2uW0TCN1bMubmJA8X88XhhlPOua4yuxRAa3xFjVf4GTYCizCij6SahLktmipWC2QdB04t89/1O/w1cDnyilFU=')
#paste your "Channel Secret" 
handler= WebhookHandler('bd870873dd0944d52f7b7b76c3479a81')

#處理訊息
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

# 處理訊息callback the same message 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
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

if __name__ == "__main__":
    app.run()