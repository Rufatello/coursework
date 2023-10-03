import requests
from datetime import datetime
import json
import os
class Vakancy:
    def __init__(self, name, page, top_n):
        self.name = name
        self.page = page
        self.top_n = top_n

    def __repr__(self):
        return f'{self.name}'

class HH(Vakancy):
    def __init__(self, name, page, top_n):
        super().__init__(name, page, top_n)

    def request_hh(self):
        self.url = 'https://api.hh.ru'
        data = requests.get(f'{self.url}/vacancies', params={'text': self.name, 'page': self.page, 'per_page': self.top_n}).json()
        return data

    def load_vacancy(self):
        data = self.request_hh()
        vacancies = []  # Список для хранения вакансий
        for vacancy in data.get('items', []):
            published_at = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z")
            vacancy_info = {
                'id': vacancy['id'],
                'name': vacancy['name'],
                'salary_ot': vacancy['salary']['from'] if vacancy.get('salary') else None,
                'salary_do': vacancy['salary']['to'] if vacancy.get('salary') else None,
                'responsibility': vacancy['snippet']['responsibility'],
                'date': published_at.strftime("%d.%m.%Y")
            }
            vacancies.append(vacancy_info)

        return vacancies

class Super_job(Vakancy):
    def __init__(self, name, page, top_n):
        super().__init__(name, page, top_n)

    def request_hh(self):
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        headers = {
                    'Host': 'api.superjob.ru',
                    'X-Api-App-Id': os.getenv('API_KEY_SJ'),
                    'Authorization': 'Bearer r.000000010000001.example.access_token',
                }
        data = requests.get(self.url, headers=headers,params={'keywords': self.name, 'page': self.page, 'count': self.top_n}).json()
        return data

    def load_vacancy(self):
        data = self.request_hh()
        vacancy_list_SJ = []
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



name = input('Введите вакансию: ')
top_n = input('Введите кол-во вакансий: ')
page = int(input('Введите страницу: '))
hh_instance = HH(name, page, top_n)
sj_instance = Super_job(name, page, top_n)
combined_dict = {'HH': hh_instance.load_vacancy(), 'SJ': sj_instance.load_vacancy()}

def load_json(combined_dict):
    with open('Super_job.json', 'w', encoding='utf-8') as file:
        json.dump(combined_dict, file, ensure_ascii=False, indent=2)
load_json(combined_dict)
platforma = input('введите платформу для поиска: (1 - HH, 2 - SJ, 3 - обе платформы)  ')
if platforma =='3':
    while True:
        hh_instance.page = page
        sj_instance.page = page
        hh_data = hh_instance.load_vacancy()
        sj_data = sj_instance.load_vacancy()

        combined_dict['HH'] = hh_data
        combined_dict['SJ'] = sj_data

        with open('Super_job.json', 'w', encoding='utf-8') as file:
            json.dump(combined_dict, file, ensure_ascii=False, indent=2)

        for platform, data in combined_dict.items():
            print(f"Платформа: {platform}")
            for item in data:
                print(item)

        a = input('перейти на следующую страницу? y/n ')
        if a == 'y':
            page += 1
        else:
            break
elif platforma =='1':
    while True:
        hh_instance.page = page
        sj_instance.page = page
        hh_data = hh_instance.load_vacancy()
        sj_data = sj_instance.load_vacancy()

        combined_dict['HH'] = hh_data
        combined_dict['SJ'] = sj_data

        with open('Super_job.json', 'w', encoding='utf-8') as file:
            json.dump(combined_dict, file, ensure_ascii=False, indent=2)

        for platform in combined_dict['HH']:
            print(f"{platform}")

        a = input('перейти на следующую страницу? y/n ')
        if a == 'y':
            page += 1
        else:
            break

else:
    while True:
        hh_instance.page = page
        sj_instance.page = page
        hh_data = hh_instance.load_vacancy()
        sj_data = sj_instance.load_vacancy()

        combined_dict['HH'] = hh_data
        combined_dict['SJ'] = sj_data

        with open('Super_job.json', 'w', encoding='utf-8') as file:
            json.dump(combined_dict, file, ensure_ascii=False, indent=2)

        for platform in combined_dict['SJ']:
            print(f"{platform}")

        a = input('перейти на следующую страницу? y/n ')
        if a == 'y':
            page += 1
        else:
            break
