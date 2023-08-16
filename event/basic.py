from line_bot_api import *


def about_us_event(event):
    emojis = [
        {
            "index": 0,
            "productId": "5ac21a18040ab15980c9b43e",
            "emojiId": "009"
        },
        {
            "index": 14,
            "productId": "5ac21a18040ab15980c9b43e",
            "emojiId": "014"
        }
    ]

    info_message = TextSendMessage(
        text="$ 史都客 Finance $\n"
             "我被設定為財經小幫手~\n"
             "下方選單有：\n"
             "股票查詢、使用說明\n"
             "使用上有任何問題可以參考使用說明",
        emojis=emojis
    )

    sticker_message = StickerSendMessage(
        package_id="11537", sticker_id="52002735"
    )

    line_bot_api.reply_message(
        event.reply_token,
        [info_message, sticker_message]
    )

