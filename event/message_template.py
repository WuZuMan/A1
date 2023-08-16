from line_bot_api import *
from event.mongodb_connection import *


def create_buttons_template():
    # 定義 Postback Action 的 data 參數
    postback_data = {
        "action": "button_clicked",
        "input_option": "openKeyboard",
        "fill_in_text": "股票查詢#"
    }

    # 將 data 參數轉換為字串形式
    postback_data_str = "&".join([f"{key}={value}" for key, value in postback_data.items()])

    # 創建一個 Postback Action 按鈕，將 data 參數添加進去
    input_postback_action = PostbackAction(
        label='輸入"#" + "股票代號"',
        data=postback_data_str
    )

    finish_postback_action = PostbackAction(
        label='結束',
        data=postback_data_str
    )

    message_template = TemplateSendMessage(
        alt_text='按鈕範本',
        template=ButtonsTemplate(
            text='請選擇下一步',
            actions=[
                input_postback_action,
                finish_postback_action
            ]
        )
    )
    return message_template


def create_quick_reply():
    message_template = TextSendMessage(
        text="下一步：下方按鈕選擇功能",
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=PostbackAction(label="請輸入股票代號", data="data=None",
                                                       input_option="openKeyboard", fill_in_text="股票查詢#")),
                QuickReplyButton(action=MessageAction(label='結束', text='結束')),
            ]
        )
    )

    return message_template


def create_image_carousel_template(user_id, code, url):
    carousel_columns = []

    # 創建 6 個 Image Carousel Columns
    # 1
    image_url_1 = "https://i.imgur.com/3daCk3V.jpg"  # 替換為實際圖片的 URL
    column_1 = ImageCarouselColumn(
        image_url=image_url_1,
        action=URITemplateAction(
            label=f'即時股價 & K線圖',
            uri=url)
    )
    carousel_columns.append(column_1)

    # 2
    basic_postback_data = {
        "action": "image_clicked",
        "data": "fetch_basic_information",
        "userID": user_id,
        "code": code
    }
    postback_data_str = "&".join([f"{key}={value}" for key, value in basic_postback_data.items()])

    image_url = "https://i.imgur.com/3daCk3V.jpg"  # 替換為實際圖片的 URL
    column = ImageCarouselColumn(
        image_url=image_url,
        action=PostbackAction(label="基本資訊", data=postback_data_str)
    )
    carousel_columns.append(column)

    # 創建 Image Carousel Template
    image_carousel_template = ImageCarouselTemplate(columns=carousel_columns)

    return TemplateSendMessage(
        alt_text='Image Carousel Template',
        template=image_carousel_template
    )


def create_flex_template(user_id, code, basic_data):
    """
    建立flex message template
    :param user_id: 使用這ID
    :param code: 股票代碼
    :param basic_data: 基本資訊
    :return: flex message
    """

    trade_market = load_stock_market(code)[0]

    if trade_market["上市/櫃"] == "上市":
        market = "TWSE"
    else:
        market = "TPEX"

    img_list = ["https://i.imgur.com/Ekn6X5E.png/img",
                "https://i.imgur.com/Ekn6X5E.png/img",
                "https://i.imgur.com/Ekn6X5E.png/img",
                "https://i.imgur.com/Ekn6X5E.png/img",
                ]
    title_list = ["即時股價日K",
                  "財務總攬",
                  "新聞",
                  "三大法人",
                  ]
    button_action_list = [
        {
            "type": "uri",
            "label": "前往TradingView",
            "uri": f"https://tw.tradingview.com/chart/?symbol={market}%3A{code}"
        },
        {
            "type": "uri",
            "label": "前往財務總攬",
            "uri":  f"https://tw.tradingview.com/symbols/{market}-{code}/financials-overview/"
        },
        {
            "type": "uri",
            "label": "前往相關新聞",
            "uri": f"https://tw.tradingview.com/symbols/{market}-{code}/news/"
        },
        {
            "type": "postback",
            "label": "三大法人彙整",
            "data": f"action=button_clicked&data=fetch_3_insti&userID={user_id}&code={code}&market={trade_market['上市/櫃']}"
        },
    ]
    bg_list = ["#03303Acc", "#9C8E7Ecc", "#03303Acc", "#9C8E7Ecc"]

    flex_content = []
    for i in range(len(img_list)):
        flex_page = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "url": img_list[i],
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "2:3",
                                "gravity": "top"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": title_list[i],
                                                "size": "xl",
                                                "color": "#ffffff",
                                                "weight": "bold"
                                            },
                                            {
                                                "type": "button",
                                                "action": button_action_list[i],
                                                "style": "primary"
                                            }
                                        ]
                                    }
                                ],
                                "position": "absolute",
                                "offsetBottom": "0px",
                                "offsetStart": "0px",
                                "offsetEnd": "0px",
                                "backgroundColor": bg_list[i],
                                "paddingAll": "20px",
                                "paddingTop": "18px"
                            }
                        ],
                        "paddingAll": "0px"
                    }
                }

        flex_content.append(flex_page)

    if basic_data != None:
        basic_info = []
        for key, value in basic_data.items():
            info = {
                "type": "text",
                "text": f"{key}: {value}",
                "offsetTop": "70px",
                "offsetStart": "4px",
                "size": "22px",
                "color": "#333333",
                "weight": "bold"
            }

            basic_info.append(info)

        text_page = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "image",
                        "url": "https://i.imgur.com/VGKRrOR.png/img",
                        "size": "full",
                        "aspectMode": "cover",
                        "aspectRatio": "2:3",
                        "gravity": "top"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "基本資訊",
                                        "size": "xl",
                                        "color": "#ffffff",
                                        "weight": "bold"
                                    },
                                    {
                                        "type": "button",
                                        "action": {
                                            "type": "postback",
                                            "label": "傳至聊天室",
                                            "data": f"action=button_clicked&data=fetch_basic_information&userID={user_id}&code={code}"
                                        },
                                        "style": "primary"
                                    }
                                ]
                            }
                        ],
                        "position": "absolute",
                        "offsetBottom": "0px",
                        "offsetStart": "0px",
                        "offsetEnd": "0px",
                        "backgroundColor": "#03303Acc",
                        "paddingAll": "20px",
                        "paddingTop": "18px"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": basic_info,
                        "position": "absolute",
                        "flex": 0,
                        "width": "264px",
                        "height": "294px",
                        "offsetTop": "18px",
                        "offsetStart": "18px",
                        "cornerRadius": "10px"
                    }
                ],
                "paddingAll": "0px"
            }
        }

        flex_content.append(text_page)

    flex_message = FlexSendMessage(
        alt_text="股票查詢",
        contents={
            "type": "carousel",
            "contents": flex_content
        }
    )

    return flex_message
