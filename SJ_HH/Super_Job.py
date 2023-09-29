import requests
import json
import os


class SuperJob:
    def __init__(self, name): #,profesion, data_vacancy, candidate, company):
        self.name = name
        self.url = 'https://api.superjob.ru/2.0/vacancies/'

    def request_super_job(self):
        headers = {
            'Host': 'api.superjob.ru',
            'X-Api-App-Id': os.getenv('API_KEY_SJ'),
            'Authorization': 'Bearer r.000000010000001.example.access_token',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = requests.get(self.url, headers = headers, params={'keyword': self.name}).json()
        super_job = {'id': data['objects'][0]['id'],
                    'profession': data['objects'][0]['profession'],
                    'data_vacansy': data['objects'][0]['date_pub_to'],
                    'candidate': data['objects'][0]['candidat'],
                    'company': data['objects'][0]["client"]["title"]}
        return data, super_job

    @staticmethod
    def load_json(fil, data):
        with open(fil, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

b = input('введите интерисующие Вас вакансию ')

a = SuperJob(b)
data, s = a.request_super_job()
job_data = data
a.load_json('Super_job.json', job_data)
print(s) #