import requests
from bs4 import BeautifulSoup
import csv
import os
import datetime

now = datetime.datetime.now()

get_answer = input('Choose what do you want to know? ')


URL_MAIN = 'https://www.hltv.org'
URL_EVENTS = 'https://www.hltv.org/events'
DICTIONARY = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; '
                            'Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 '
                            'Safari/537.36 OPR/73.0.3856.438', 'accept': '*/*'}
FILE = 'parser.csv'


def get_html(url, params=None):
    response = requests.get(url, headers=DICTIONARY, params=params)
    return response


def get_data_rating(html):
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find('a', {"class": "block button text-center"}).get_text(strip=True)
    start = 0
    day = ''
    for i in range(len(item)):
        if item[i].isdigit():
            start = i
            day += item[i]
    month = item[start::].split(' ')[2]
    year = now.year
    url = 'https://www.hltv.org/ranking/teams/' + str(year) + '/' + month.lower() + '/' + day
    return url


def get_content_rating(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='ranked-team standard-box')

    teams = []
    for item in items:
        teams.append({
            'name': item.find('span', class_='name').get_text(strip=True),
            'position': item.find('span', class_='position').get_text(strip=True).replace('#', ''),
            'points': item.find('span', class_='points').get_text(strip=True),
            'logo': item.find('img').get('src'),
        })
    return teams


def get_content_events(html, kind):
    soup = BeautifulSoup(html, 'html.parser')
    if kind == 'TODAY':
        main = soup.find('div', {"id": "TODAY"})
    elif kind == 'FEATURED':
        main = soup.find('div', {"id": "FEATURED"})
    else:
        main = soup.find('div', {"id": "ALL"})
    items = main.find_all('a', class_='a-reset ongoing-event')
    events = []
    for item in items:
        events.append({
            'name': item.find('div', class_='text-ellipsis').get_text(strip=True),
            'data': item.find('span', class_='col-desc').get_text(strip=True),
            'logo': item.find('img', class_='logo').get('src'),
        })
    return events


def get_content_news(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', {"class": "newsline article"})
    news = []
    for i in range(len(items)):
        news.append({
            'text': items[i].find('div', {"class": "newstext"}).get_text(strip=True),
            'src': 'https://www.hltv.org' + items[i].get('href'),
            'data': items[i].find('div', {"class": "newsrecent"}).get_text(strip=True),
        })
    return news


def get_content_matches(html):
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find('div', {"class": "rightCol"})
    items2 = item.find_all('a', {"class": "hotmatch-box a-reset"})
    matches = []

    for i in range(len(items2)):
        matches.append({
            'name1': items2[i].find_all('span', {"class": "team"})[0].get_text(strip=True),
            'flag1': items2[i].find_all('img', {"class": "flag"})[0].get('src'),
            'name2': items2[i].find_all('span', {"class": "team"})[1].get_text(strip=True),
            'flag2': items2[i].find_all('img', {"class": "flag"})[1].get('src'),
            'count_or_time': items2[i].find_all('div', {"class": "livescore twoRowExtraRow"}).get_text(strip=True) if
            items2[i].text.count('livescore twoRowExtraRow') >= 2 else 0
        })

    return matches


def save_file_rating(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Position', 'Logo', 'Team', 'Points'])
        for item in items:
            writer.writerow([item['position'], 'img', item['name'], item['points']])


def save_file_events(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Name', 'Date', 'Logo'])
        for item in items:
            writer.writerow([item['name'], item['data'], 'img'])


def save_file_news(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Topic', 'SRC', 'Data'])
        for item in items:
            writer.writerow([item['text'], item['src'], item['data']])


def save_file_matches(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Name1', 'Flag1', 'Name2', 'Flag2', 'Count-Time'])
        for item in items:
            writer.writerow([item['name1'], item['flag1'], item['name2'], item['flag2'], item['count_or_time']])


def parse():
    if get_answer == 'Rating':
        html_0 = get_html(URL_MAIN)
        if html_0.status_code == 200:
            url_rating = get_data_rating(html_0.text)
            html = get_html(url_rating)
            if html.status_code == 200:
                teams = get_content_rating(html.text)
                save_file_rating(teams, FILE)
                os.startfile(FILE)
            else:
                print('Error')
        else:
            print('Error')
    elif get_answer == 'Events':
        get_answer_2 = input('Enter what type of events do you want to see: ')
        html = get_html(URL_EVENTS)
        if html.status_code == 200:
            events = get_content_events(html.text, get_answer_2)
            save_file_events(events, FILE)
            os.startfile(FILE)
        else:
            print('Error')
    elif get_answer == 'Matches':
        html = get_html(URL_MAIN)
        if html.status_code == 200:
            matches = get_content_matches(html.text)
            save_file_matches(matches, FILE)
            os.startfile(FILE)
        else:
            print('Error')
    elif get_answer == 'News':
        year = input('Enter year of news: ')
        month = input('Enter month of news: ')
        url_news = 'https://www.hltv.org/news/archive/' + year + '/' + month
        html = get_html(url_news)
        if html.status_code == 200:
            news = get_content_news(html.text)
            save_file_news(news, FILE)
            os.startfile(FILE)
        else:
            print('Error')
    else:
        print("Sorry, but this program doesn't know how to complete your request :(")


parse()
