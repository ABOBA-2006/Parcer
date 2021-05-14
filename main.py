import requests
from bs4 import BeautifulSoup


URL = 'https://www.hltv.org/'
DICTIONARY = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; '
                            'Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 '
                            'Safari/537.36 OPR/73.0.3856.438', 'accept': '*/*'}


def get_html(url, params=None):
    response = requests.get(url, headers=DICTIONARY, params=params)
    return response


def parse():
    html = get_html(URL)
    print(html)


parse()
