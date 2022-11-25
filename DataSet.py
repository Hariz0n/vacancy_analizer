from Vacancy import Vacancy
from Salary import Salary
import csv
import re


class DataSet:
    def __init__(self, file_name):
        self.file_name: str = file_name
        self.vacancies_objects: list[Vacancy] = self.csv_parser()

    def csv_parser(self):
        headers = None
        vacancies_list = []
        with open(self.file_name, 'r', encoding='utf-8-sig') as csvfile:
            file = csv.reader(csvfile)
            for line in file:
                if headers is None:
                    headers = line
                    continue
                if len(line) == len(headers) and '' not in line:
                    primitives = {}
                    salary = {}
                    for column in range(len(line)):
                        corr_value = [' '.join(re.sub(r'<[^>]+>', '', value).split()) for value in
                                      line[column].split('\n')]
                        if headers[column].startswith('salary'):
                            salary[headers[column]] = " ".join(corr_value)
                            continue
                        if headers[column] == 'key_skills':
                            primitives[headers[column]] = corr_value
                            continue
                        primitives[headers[column]] = " ".join(corr_value)
                    vacancies_list.append(Vacancy(primitives, Salary(salary)))
        if not vacancies_list:
            print('Нет данных')
        return vacancies_list

