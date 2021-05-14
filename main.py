import requests
from bs4 import BeautifulSoup

get_answer = input('Choose what do you want to know? ')


URL = 'https://www.hltv.org/'
DICTIONARY = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; '
                            'Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 '
                            'Safari/537.36 OPR/73.0.3856.438', 'accept': '*/*'}


def get_html(url, params=None):
    response = requests.get(url, headers=DICTIONARY, params=params)
    return response


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    if get_answer == 'Rating':
        item_1 = soup.find_all('div', class_='col-box rank')
        print(item_1)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')


parse()
