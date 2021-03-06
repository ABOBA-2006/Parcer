import requests
from bs4 import BeautifulSoup
import csv
import os
import datetime
from tkinter import *


now = datetime.datetime.now()

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
            'logo': 'https://www.hltv.org' +  item.find('img').get('src'),
        })
    return teams


def get_content_events(html):
    soup = BeautifulSoup(html, 'html.parser')
    # if kind == 'TODAY':
    #     main = soup.find('div', {"id": "TODAY"})
    # elif kind == 'FEATURED':
    #     main = soup.find('div', {"id": "FEATURED"})
    # else:
    main = soup.find('div', {"id": "ALL"})
    items = main.find_all('a', class_='a-reset ongoing-event')
    events = []
    for item in items:
        events.append({
            'name': item.find('div', class_='text-ellipsis').get_text(strip=True),
            'data': item.find('span', class_='col-desc').get_text(strip=True),
            'logo': 'https://www.hltv.org' + item.find('img', class_='logo').get('src'),
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
        time = 0
        counts = 0
        if not items2[i].find('div', {"class": "middleExtra"}) is None:
            time = int(items2[i].find('div', {"class": "middleExtra"}).get_text(strip=True)[:2:]) + 1
        if time == 24:
            time = 0

        # if not items2[i].find('div', {"class": "twoRowExtra"}) is None:
        #     items_count = items2[i].find_all('div', {"class": "livescore twoRowExtraRow"})
        #     print(items_count)
        #     counts = items_count[0].get_text() + items_count[1].get_text()

        matches.append({
            'name1': items2[i].find_all('span', {"class": "team"})[0].get_text(strip=True),
            'flag1': 'https://www.hltv.org' + items2[i].find_all('img', {"class": "flag"})[0].get('src'),
            'name2': items2[i].find_all('span', {"class": "team"})[1].get_text(strip=True),
            'flag2': 'https://www.hltv.org' + items2[i].find_all('img', {"class": "flag"})[1].get('src'),
            'count_or_time': str(time) + items2[i].find('div', {"class": "middleExtra"}).get_text(strip=True)[2::]
                            if not items2[i].find('div', {"class": "middleExtra"}) is None else '-------------------',
                            # counts if not items2[i].find('div', {"class": "twoRowExtra"}) is None else 0,
            'live': 'Live' if items2[i].find('div', {"class": "middleExtra"}) is None else 'Not Live',
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
        writer.writerow(['Name1', 'Flag1', 'Name2', 'Flag2', 'Time', 'Live'])
        for item in items:
            writer.writerow([item['name1'], item['flag1'], item['name2'], item['flag2'],
                             item['count_or_time'], item['live']])


root = Tk()
root.title("LGBT++")
root.minsize(width=750, height=400)

def button_1_job(event):
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


def button_2_job(event):
    html = get_html(URL_EVENTS)
    if html.status_code == 200:
        events = get_content_events(html.text)
        save_file_events(events, FILE)
        os.startfile(FILE)
    else:
        print('Error')


def button_3_job(event):
    html = get_html(URL_MAIN)
    if html.status_code == 200:
        matches = get_content_matches(html.text)
        save_file_matches(matches, FILE)
        os.startfile(FILE)
    else:
        print('Error')


def button_4_job(event):
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


def button_5_job(event):
    exit()


def main():
    but1 = Button(root,
                  text="Rating",
                  width=30,height=10,
                  bg="lightblue",fg="blue")
    but1.bind("<Button-1>", button_1_job)
    but1.place(rely=0.1, relx=0.1)


    but2 = Button(root,
                  text="Events",
                  width=30,height=10,
                  bg="lightpink",fg="purple")
    but2.bind("<Button-1>", button_2_job)
    but2.place(rely=0.1, relx=0.6)


    but3 = Button(root,
                  text="Matches",
                  width=30,height=10,
                  bg="lightgreen",fg="darkgreen")
    but3.bind("<Button-1>", button_3_job)
    but3.place(rely=0.55, relx=0.6)


    but4 = Button(root,
                  text="News",
                  width=30,height=10,
                  bg="yellow",fg="darkorange")
    but4.bind("<Button-1>", button_4_job)
    but4.place(rely=0.55, relx=0.1)


    but5 = Button(root,
                  text="Exit",
                  width=10, height=5,
                  bg="black", fg="white")
    but5.bind("<Button-1>", button_5_job)
    but5.place(rely=0.4, relx=0.45)

main()
root.mainloop()

