import requests
import twstock
import pandas as pd
import numpy as np


def fetch_stock_basic_info(code):
    """
    從twstock.codes取得股票資訊
    :param code: 股票代號
    :return: {"股票代號": "", "名稱": "", "上市/櫃日期": "", "上市/櫃": "", "類別": ""}
    """
    try:
        info = twstock.codes[f'{code}']
        useful = {
            "股票代號": info[1],
            "名稱": info[2],
            "上市/櫃日期": info[4],
            "上市/櫃": info[5],
            "類別": info[6]
        }
        return useful
    except KeyError:
        return None


def fetch_twse_3institution(code):
    """
    抓取上市股票三大法人買賣超資訊
    :param code: 股票代號
    :return:
    """
    query_url = f"https://www.twse.com.tw/rwd/zh/fund/T86?date=20230811&selectType=ALL&response=json&_=1691826664719"

    res = requests.get(query_url)

    inv_json = res.json()
    # print(inv_json)

    df = pd.DataFrame.from_dict(inv_json["data"])

    df.columns = ['證券代號', '證券名稱',
                  '外陸資買進股數(不含外資自營商)', '外陸資賣出股數(不含外資自營商)', '外陸資買賣超股數(不含外資自營商)',
                  '外資自營商買進股數', '外資自營商賣出股數', '外資自營商買賣超股數',
                  '投信買進股數', '投信賣出股數', '投信買賣超股數', '自營商買賣超股數',
                  '自營商買進股數(自行買賣)', '自營商賣出股數(自行買賣)', '自營商買賣超股數(自行買賣)',
                  '自營商買進股數(避險)', '自營商賣出股數(避險)', '自營商買賣超股數(避險)', '三大法人買賣超股數']

    filtered_df = df[df["證券代號"] == code]

    target_columns = ['證券代號', '證券名稱', '外陸資買進股數(不含外資自營商)', '外陸資賣出股數(不含外資自營商)',
                      '外陸資買賣超股數(不含外資自營商)', '投信買進股數', '投信賣出股數', '投信買賣超股數',
                      '自營商買賣超股數',
                      '自營商買進股數(自行買賣)', '自營商賣出股數(自行買賣)', '自營商買賣超股數(自行買賣)',
                      '自營商買進股數(避險)', '自營商賣出股數(避險)', '自營商買賣超股數(避險)'
                      ]

    filtered_df_todict = filtered_df[target_columns].to_dict('records')[0]

    process_dict = {
        '證券代號': filtered_df_todict["證券代號"],
        '證券名稱': filtered_df_todict["證券名稱"].replace(" ", ""),
        '外資買入張數': np.round((float(filtered_df_todict["外陸資買進股數(不含外資自營商)"].replace(",", "")) / 1000)),
        '外資賣出張數': np.round((float(filtered_df_todict["外陸資賣出股數(不含外資自營商)"].replace(",", "")) / 1000)),
        '外資買賣超': np.round((float(filtered_df_todict["外陸資買賣超股數(不含外資自營商)"].replace(",", "")) / 1000)),
        '投信買入張數': np.round((float(filtered_df_todict["投信買進股數"].replace(",", "")) / 1000)),
        '投信賣出張數': np.round((float(filtered_df_todict["投信賣出股數"].replace(",", "")) / 1000)),
        '投信買賣超': np.round((float(filtered_df_todict["投信買賣超股數"].replace(",", "")) / 1000)),
        '自營商買入張數': np.round((float(filtered_df_todict["自營商買進股數(自行買賣)"].replace(",", "")) + float(
            filtered_df_todict["自營商買進股數(避險)"].replace(",", ""))) / 1000),
        '自營商賣出張數': np.round((float(filtered_df_todict["自營商賣出股數(自行買賣)"].replace(",", "")) + float(
            filtered_df_todict["自營商賣出股數(避險)"].replace(",", ""))) / 1000),
        '自營商買賣超': np.round((float(filtered_df_todict["自營商買賣超股數"].replace(",", "")) / 1000)),
        '自營商(避險)買入張數': np.round((float(filtered_df_todict["自營商買進股數(避險)"].replace(",", "")) / 1000)),
        '自營商(避險)賣出張數': np.round((float(filtered_df_todict["自營商賣出股數(避險)"].replace(",", "")) / 1000)),
        '自營商(避險)買賣超': np.round((float(filtered_df_todict["自營商買賣超股數(避險)"].replace(",", "")) / 1000)),
    }

    return process_dict


def fetch_tpex_3institution(code):
    """
    抓取上櫃股票三大法人買賣超資訊
    :param code: 股票代號
    :return:
    """
    query_url = "https://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&se=EW&t=D&_=1691917586205"

    df = pd.read_json(query_url)
    print(len(df["aaData"]))

    columns_list = ['證券代號', '證券名稱',
                    '外陸資買進股數(不含外資自營商)', '外陸資賣出股數(不含外資自營商)', '外陸資買賣超股數(不含外資自營商)',
                    '外資自營商買進股數', '外資自營商賣出股數', '外資自營商買賣超股數',
                    '外資及陸資買進股數', '外資及陸資賣出股數', '外資及陸資買賣超股數',
                    '投信買進股數', '投信賣出股數', '投信買賣超股數',
                    '自營商買進股數(自行買賣)', '自營商賣出股數(自行買賣)', '自營商買賣超股數(自行買賣)',
                    '自營商買進股數(避險)', '自營商賣出股數(避險)', '自營商買賣超股數(避險)',
                    '自營商買進股數', '自營商賣出股數', '自營商買賣超股數',
                    '三大法人買賣超股數', "EE"
                    ]

    processed_df = pd.DataFrame(columns=columns_list)
    # print(processed_df)

    # for i in zip(columns_list, df["aaData"][0]):
    #     print(i)
    # print(len(df["aaData"][0]))
    #
    # print(len(columns_list))

    for i, row in df.iterrows():
        nd_array = np.array(row["aaData"])
        nd_array.reshape((1, 25))

        processed_df.loc[len(processed_df.index)] = nd_array

    # print(processed_df.to_string())

    filtered_df = processed_df[processed_df["證券代號"] == code]
    # print(filtered_df.to_string())

    target_columns = ['證券代號', '證券名稱',
                      '外陸資買進股數(不含外資自營商)', '外陸資賣出股數(不含外資自營商)', '外陸資買賣超股數(不含外資自營商)',
                      '投信買進股數', '投信賣出股數', '投信買賣超股數',
                      '自營商買進股數(自行買賣)', '自營商賣出股數(自行買賣)', '自營商買賣超股數(自行買賣)',
                      '自營商買進股數(避險)', '自營商賣出股數(避險)', '自營商買賣超股數(避險)',
                      '自營商買賣超股數',
                      ]

    filtered_df_todict = filtered_df[target_columns].to_dict('records')[0]
    # print(filtered_df_todict)

    process_dict = {
        '證券代號': filtered_df_todict["證券代號"],
        '證券名稱': filtered_df_todict["證券名稱"].replace(" ", ""),
        '外資買入張數': np.round((float(filtered_df_todict["外陸資買進股數(不含外資自營商)"].replace(",", "")) / 1000)),
        '外資賣出張數': np.round((float(filtered_df_todict["外陸資賣出股數(不含外資自營商)"].replace(",", "")) / 1000)),
        '外資買賣超': np.round((float(filtered_df_todict["外陸資買賣超股數(不含外資自營商)"].replace(",", "")) / 1000)),
        '投信買入張數': np.round((float(filtered_df_todict["投信買進股數"].replace(",", "")) / 1000)),
        '投信賣出張數': np.round((float(filtered_df_todict["投信賣出股數"].replace(",", "")) / 1000)),
        '投信買賣超': np.round((float(filtered_df_todict["投信買賣超股數"].replace(",", "")) / 1000)),
        '自營商買入張數': np.round((float(filtered_df_todict["自營商買進股數(自行買賣)"].replace(",", "")) + float(
            filtered_df_todict["自營商買進股數(避險)"].replace(",", ""))) / 1000),
        '自營商賣出張數': np.round((float(filtered_df_todict["自營商賣出股數(自行買賣)"].replace(",", "")) + float(
            filtered_df_todict["自營商賣出股數(避險)"].replace(",", ""))) / 1000),
        '自營商買賣超': np.round((float(filtered_df_todict["自營商買賣超股數"].replace(",", "")) / 1000)),
        '自營商(避險)買入張數': np.round((float(filtered_df_todict["自營商買進股數(避險)"].replace(",", "")) / 1000)),
        '自營商(避險)賣出張數': np.round((float(filtered_df_todict["自營商賣出股數(避險)"].replace(",", "")) / 1000)),
        '自營商(避險)買賣超': np.round((float(filtered_df_todict["自營商買賣超股數(避險)"].replace(",", "")) / 1000)),
    }

    return process_dict


if __name__ == "__main__":
    code = "3483"
    print(fetch_tpex_3institution_v2(code))
