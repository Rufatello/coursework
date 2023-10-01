import requests
import json
import os
from datetime import datetime
BASE_URL = 'https://api.hh.ru'


l = input('Введите вакансию')
page = 1


test = []
class SuperJob:
    def __init__(self):  # ,profesion, data_vacancy, candidate, company):

        self.url = 'https://api.superjob.ru/2.0/vacancies/'

    def request_super_job(self):
        headers = {
            'Host': 'api.superjob.ru',
            'X-Api-App-Id': os.getenv('API_KEY_SJ'),
            'Authorization': 'Bearer r.000000010000001.example.access_token',
        }
        data = requests.get(self.url, headers=headers, params={'keyword': l}).json()

        for i in data['objects']:
            super_job = {
                'id': i['id'],
                'profession': i.get('profession', ''),
                'data_vacansy': i.get('date_pub_to', ''),
                'candidate': i.get('candidat', ''),
                'company': i.get('title', '')
            }
        return data, super_job


    @staticmethod
    def load_json(fil, data):
        with open(fil, 'w', encoding='utf-8') as file:
            json.dump(s, file, ensure_ascii=False, indent=2)


a = SuperJob()
data, s = a.request_super_job()
job_data = data
a.load_json('SJ_HH\Super_job.json', job_data)
print(s)

def request_hh():
    data = requests.get(f'{BASE_URL}/vacancies', params={'text': l,  'page' : page, 'per_page':50}).json()
    return data

r = request_hh()

def load_json(fil):
    with open(fil, 'w', encoding='utf-8') as file:
        json.dump(r, file, ensure_ascii=False, indent=2)
load_json('SJ_HH\HH.json')

while True:
    r = request_hh()
    for vacancy in r.get('items', []):
        published_at = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z")
        if vacancy.get('salary'):
            spisok = {
                'id': vacancy['id'],
                'name': vacancy['name'],
                'salary': vacancy['salary']['from'] if vacancy.get('salary') else None,
                'solary_do': vacancy['salary']['to'] if vacancy.get('salary') else None,
                'responsibility': vacancy['snippet']['responsibility'],
                'data': published_at.strftime("%d.%m.%Y")
            }
            print(spisok)

    p = input('добавить еще одну страницу? y/n ')
    if p == 'y':
        page += 1
        continue
    else:
        break

