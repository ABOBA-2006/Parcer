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
        items = soup.find_all('div', class_='col-box rank')

        teams = []
        for item in items:
            teams.append({
                'name': item.find('a', class_='text-ellipsis').get_text(strip=True),
                'position': item.find('a', class_='rankNum').get_text(strip=True).replace('.', ''),
                'logo': item.find('img', class_='teamImg').get('src')
            })
        print(teams)
    else:
        print("Sorry, but this program doesn't know how to complete your request :(")


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')


parse()
