from line_bot_api import *
from event.basic import *
from event.message_template import *
from event.request_event import *
import re
import datetime
import time

app = Flask(__name__)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id  # 使用者id
    user_name = profile.display_name  # 使用者名稱
    # print(uid, user_name)

    message_text = str(event.message.text).lower()

    # --------------------股價查詢--------------------
    # listening_code = False
    if message_text == "股票查詢":
        message = create_quick_reply()
        line_bot_api.push_message(uid, message)

    if re.match(r"股票查詢#\d", message_text):
        stock_number = message_text[5:].upper()
        line_bot_api.push_message(uid, TextSendMessage(text=f"{stock_number}搜尋中..."))
        basic_data = fetch_stock_basic_info(stock_number)
        flex_message_template = create_flex_template(uid, stock_number, basic_data)
        line_bot_api.push_message(uid, flex_message_template)

    # --------------------@使用說明------------------
    if message_text == "@使用說明":
        about_us_event(event)


@handler.add(PostbackEvent)
def handle_postback(event):
    # 解析 Postback 事件的 data 參數
    postback_data = event.postback.data
    # 解析 data 參數，這可能是一個字串，需要根據情況進行分割和解析
    postback_params = dict(param.split('=') for param in postback_data.split('&'))

    # --------------------當使用者在股票旋轉圖片中選取基本資訊時的postback處理------------------
    if postback_params["data"] == "fetch_basic_information":
        line_bot_api.push_message(postback_params["userID"], TextSendMessage(text=f"基本資料搜尋中..."))
        basic_data = fetch_stock_basic_info(postback_params["code"])
        basic_data_str = ""
        for key, value in basic_data.items():
            basic_data_str += f"{key}: {value}\n"

        line_bot_api.push_message(postback_params["userID"], TextSendMessage(text=basic_data_str))

    # --------------------當使用者在股票旋轉圖片中選取三大法人時的postback處理------------------
    if postback_params["data"] == "fetch_3_insti":
        line_bot_api.push_message(postback_params["userID"], TextSendMessage(text=f"三大法人資料搜尋中..."))

        if postback_params["market"] == "上市":
            institution_data = fetch_twse_3institution(postback_params["code"])
        else:
            institution_data = fetch_tpex_3institution(postback_params["code"])

        institution_str = ""
        for key, value in institution_data.items():
            institution_str += f"{key}: {value}\n"

        line_bot_api.push_message(postback_params["userID"], TextSendMessage(text=institution_str))


@handler.add(FollowEvent)
def handle_follow(event):
    pass


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print(event)


if __name__ == "__main__":
    app.run()
