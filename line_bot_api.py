#載入linebot 所需的套件
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler, exceptions)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *        #* means all

# paste your "Channel Access Token"
line_bot_api = LineBotApi('Hr4OfRuaES7MBwy/6a2FC3tDKTQrfzgutDKQ1gXaZ5qwkIyb9TbGlk2xgNbMNzIjmewn6u9nX8pn5hwWul7HED2uW0TCN1bMubmJA8X88XhhlPOua4yuxRAa3xFjVf4GTYCizCij6SahLktmipWC2QdB04t89/1O/w1cDnyilFU=')
#paste your "Channel Secret" 
handler= WebhookHandler('bd870873dd0944d52f7b7b76c3479a81')