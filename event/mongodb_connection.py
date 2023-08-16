from pymongo import MongoClient
import datetime
from dotenv import load_dotenv
import os

stockDB = "line_bot_project"
# collection = "stock"


def constructor_stock():
    """
    建立MongoDB的連線
    :return: db
    """
    load_dotenv()
    key = os.environ['MONGODB_URI']
    client = MongoClient(key)
    db = client[stockDB]
    return db


def load_stock_market(code):
    """
    處理上市、上櫃分類
    :param: code: 股票代碼
    :return: db collect
    """
    db = constructor_stock()

    collect = db["market_type"]
    company = collect.find({"代號": f"{code}"})

    return company


if __name__ == "__main__":
    target = load_stock_market("00878")

    print(target[0])

    # for i in target:
    #     print(i)
