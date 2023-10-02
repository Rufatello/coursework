from abc import ABC, abstractmethod
import os
import json
import requests
from datetime import datetime
name_vacancy = input('Введите вакансию: ')
top_n = int(input('Введите количество вакансий для просмотра: '))
page = 1
vacancy_list_HH = []
vacancy_list_SJ = []
class Vacancy(ABC):
    @abstractmethod
    def load_vacancy(self):
        pass


class Super_job(Vacancy):

    def request_hh(self):
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        headers = {
                    'Host': 'api.superjob.ru',
                    'X-Api-App-Id': os.getenv('API_KEY_SJ'),
                    'Authorization': 'Bearer r.000000010000001.example.access_token',
                }
        data = requests.get(self.url, headers=headers,params={'keywords': name_vacancy, 'page': page, 'count': top_n}).json()
        return data

    def load_vacancy(self):
        data = self.request_hh()
        for i in data['objects']:
            published_at = datetime.fromtimestamp(i.get('date_published', ''))
            super_job = {
                'id': i['id'],
                'name': i.get('profession', ''),
                'solary_ot': i.get('payment_from', '') if i.get('payment_from') else None,
                'solary_do': i.get('payment_to') if i.get('payment_to') else None,
                'responsibility': i.get('candidat').replace('\n', '').replace('•', '') if i.get('candidat') else None,
                'data': published_at.strftime("%d.%m.%Y"),

            }
            vacancy_list_SJ.append(super_job)
        return vacancy_list_SJ


class HeadHunter(Vacancy):

    def request_hh(self):
        self.url = 'https://api.hh.ru'
        data = requests.get(f'{self.url}/vacancies', params={'text': name_vacancy, 'page': page, 'per_page': top_n}).json()
        return data

    def load_vacancy(self):
        data = self.request_hh()
        for vacancy in data.get('items', []):
            published_at = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z")
            spisok = {
                'id': vacancy['id'],
                'name': vacancy['name'],
                'salary_ot': vacancy['salary']['from'] if vacancy.get('salary') else None,
                'solary_do': vacancy['salary']['to'] if vacancy.get('salary') else None,
                'responsibility': vacancy['snippet']['responsibility'],
                'data': published_at.strftime("%d.%m.%Y")
            }
            vacancy_list_HH.append(spisok)
        return vacancy_list_HH



def test_go(vacansy):
    vacansy.load_vacancy()
sj = Super_job()
hh= HeadHunter()
test_go(sj)
test_go(hh)
combined_dict = {'HH':vacancy_list_HH, 'SJ': vacancy_list_SJ}

def load_json(fil, combined_dict):
    with open(fil, 'w', encoding='utf-8') as file:
        json.dump(combined_dict, file, ensure_ascii=False, indent=2)

load_json('Super_job.json', combined_dict)

platforms = input('Введите платформу для отображения информации (пример: hh или sj): ').lower()
if platforms == 'hh':
    while True:
        hh = HeadHunter()
        hh_data = hh.load_vacancy()
        with open('Super_job.json', 'r') as f:
            data = json.load(f)
            for i in data['HH']:
                print(i)
        page_list = input('Перейти на другую страницу? y/n ')
        if page_list == 'y':
            page += 1
            print(page)
            continue
        else:
            break
elif platforms == 'sj':
    while True:
        hh = HeadHunter()
        hh_data = hh.load_vacancy()
        with open('Super_job.json', 'r') as f:
            data = json.load(f)
            for i in data['SJ']:
                print(i)
        page_list = input('Перейти на другую страницу? y/n ')
        if page_list == 'y':
            page += 1
            print(page)  
            continue
        else:
            break
