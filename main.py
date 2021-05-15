import requests
from bs4 import BeautifulSoup
import csv
import os

get_answer = input('Choose what do you want to know? ')


URL_RATING = 'https://www.hltv.org/ranking/teams/2021/may/10'
URL_EVENTS = 'https://www.hltv.org/events'
URL_MATCHES = 'https://www.hltv.org/matches'
DICTIONARY = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; '
                            'Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 '
                            'Safari/537.36 OPR/73.0.3856.438', 'accept': '*/*'}
FILE = 'teams_rating-events.csv'


def get_html(url, params=None):
    response = requests.get(url, headers=DICTIONARY, params=params)
    return response


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


# def get_content_matches(html, date):
#     soup = BeautifulSoup(html, 'html.parser')
#     items = soup.find_all('div', {"class": "upcomingMatchesSection"})
#     items2 = items.find_all('div', {"class": "matchDayHeadline"})
#     matches = []
#     for i in range(len(items)):
#         if date == items2[i]:
#             items3 = items[i].find('div', {"class": "matchTeam team1"})
#             items4 = items[i].find('div', {"class": "matchTeam team2"})
#             matches.append({
#                 'first_team': items3[i].find('div', class_='matchTeamName text-ellipsis').get_text(strip=True),
#                 'second_team': items4[i].find('div', class_='matchTeamName text-ellipsis').get_text(strip=True),
#                 'logo_1': items3[i].find('img').get('src'),
#                 'logo_2': items4[i].find('img').get('src'),
#             })
#     return matches


def save_file_rating(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Position', 'Logo', 'Team', 'Points'])
        for item in items:
            writer.writerow([item['position'], 'img', item['name'], item['points']])


def save_file_events(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Name', 'Date', 'Logo'])
        for item in items:
            writer.writerow([item['name'], item['data'], 'img'])


def parse():
    if get_answer == 'Rating':
        html = get_html(URL_RATING)
        if html.status_code == 200:
            teams = get_content_rating(html.text)
            save_file_rating(teams, FILE)
            os.startfile(FILE)
        else:
            print('Error')
    elif get_answer == 'Events':
        get_answer_2 = input('Enter what type of events do you want to see: ')
        html = get_html(URL_EVENTS)
        with open('test.html', 'w') as file:
            file.write(html.text)
        if html.status_code == 200:
            events = get_content_events(html.text, get_answer_2)
            save_file_events(events, FILE)
            os.startfile(FILE)
        else:
            print('Error')
    else:
        print("Sorry, but this program doesn't know how to complete your request :(")


parse()
