import requests
from bs4 import BeautifulSoup

def oil_price():
    Target_url = "https://gas.goodlife.tw/"
    rs = requests.session()
    res = rs.get(Target_url, verify=False)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")
    title = soup.select("#main")[0].text.replace('\n','').split('(')[0]
    gas_price = soup.select("#gas-price")[0].text.replace('\n\n\n','').replace(' ','')[0]
    cpc = soup.select('#cpc')[0].text.replace(' ','')
    content = '{}\n{}{}'.format(title.gas_price, cpc)
    return content