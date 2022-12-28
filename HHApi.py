import pandas as pd
import requests
from datetime import datetime


class HHApi:
    url = 'https://api.hh.ru/vacancies'

    def getVacancies(self, day: datetime):
        result = []
        for hour in range(0, 23):
            response = requests.get(url=self.url, headers={}, params={
                'specialization': 1,
                "date_from": f"{day.year}-{day.month}-{day.day}T{str(hour).zfill(2)}:00:00+0300",
                "date_to": f"{day.year}-{day.month}-{day.day}T{str(hour + 1).zfill(2)}:59:00+0300"
            })
            print(response.json()['found'])
            for page in range((response.json()['found'] // 100) + 1):
                data = requests.get(url=self.url, headers={}, params={
                    'specialization': 1,
                    'found': 1,
                    'per_page': 100,
                    'page': page,
                    "date_from": f"{day.year}-{day.month}-{day.day}T{str(hour).zfill(2)}:00:00+0300",
                    "date_to": f"{day.year}-{day.month}-{day.day}T{str(hour + 1).zfill(2)}:59:00+0300"
                }).json()
                for vacancy in data['items']:
                    salary = vacancy['salary'] or {}
                    result.append([vacancy["name"], salary.get("from"),
                                   salary.get("to"), salary.get("currency"),
                                   vacancy["area"]["name"], vacancy["published_at"]])
        ret = pd.DataFrame(result,
                           columns=['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at'])
        ret.to_csv('HeadHunter Vacs.csv', index=False)
        return ret


HHApi().getVacancies(datetime(2022, 12, 27))
