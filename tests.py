from unittest import TestCase

from DataSet import DataSet
from Salary import Salary
from Vacancy import Vacancy
from Statistics import Statistic


class SalaryTests(TestCase):
    def test_all_types_correct(self):
        sObj = Salary({
            "salary_from": 1000,
            "salary_to": 5000,
            "salary_gross": 'False',
            "salary_currency": "RUR"
        })
        self.assertTrue(type(sObj.salary_to) == int, 'Нижний оклад не integer')
        self.assertTrue(type(sObj.salary_from) == int, 'Верхний оклад не integer')
        self.assertTrue(type(sObj.salary_gross) == str, 'Gross не str')
        self.assertTrue(type(sObj.salary_currency) == str, 'Валюта не str')
        self.assertTrue(type(sObj.salary_average) == int, 'Средняя зарплата не int')

    def test_correct_average(self):
        sObj = Salary({
            "salary_from": 1000,
            "salary_to": 5000,
            "salary_gross": 'False',
            "salary_currency": "RUR"
        })

        self.assertTrue(sObj.salary_average == 3000, 'Не правильно посчитана средняя зарплата')

    def test_correct_currency_convert(self):
        self.assertTrue(
            Salary({'salary_from': 1000, 'salary_to': 1000, 'salary_currency': "USD"}).convert_currency_average(),
            60660.0)


class VacancyTests(TestCase):
    static_salary = Salary({
        "salary_from": 1000,
        "salary_to": 5000,
        "salary_gross": 'False',
        "salary_currency": "RUR"
    })
    static_Vacancy = Vacancy({
        'name': 'designer',
        "description": 'UI\\UX designer',
        'key_skills': ['Photoshop', 'figma'],
        'experience_id': 'between1And3',
        'premium': 'False',
        'employer_name': 'Naumen',
        'area_name': 'Prague',
        'published_at': '2022-07-05T18:19:30+0300'
    }, static_salary)

    def test_all_types_correct(self):
        self.assertTrue(type(self.static_Vacancy.name) == str)
        self.assertTrue(type(self.static_Vacancy.description) == str)
        self.assertTrue(type(self.static_Vacancy.key_skills) == list)
        self.assertTrue(type(self.static_Vacancy.experience_id) == str)
        self.assertTrue(type(self.static_Vacancy.premium) == str)
        self.assertTrue(type(self.static_Vacancy.employer_name) == str)
        self.assertTrue(type(self.static_Vacancy.area_name) == str)
        self.assertTrue(type(self.static_Vacancy.published_at) == str)


class DataSetTests(TestCase):

    def test_correct_type_return(self):
        try:
            dataset = DataSet('test.csv')
            self.assertEqual(type(dataset.vacancies_objects), list, 'Неправильно обработан csv файла')
        except:
            self.fail('No such file: test.csv')

    def test_correct_parsing(self):
        try:
            dataset = DataSet('test.csv')
            self.assertEqual(len(dataset.vacancies_objects), 5, 'Не обработаны строки с пустыми файлами')
        except:
            self.fail('No such file: test.csv')

    def test_empty_file(self):
        try:
            dataset = DataSet('empty.csv')
            self.assertEqual(len(dataset.vacancies_objects), 0, 'Неправильно обработан csv файла')
        except:
            self.fail('No such file: empty.csv')


class StatisticTests(TestCase):

    def test_correct_statistics(self):
        try:
            dataset = DataSet('test.csv')
        except:
            self.fail('No such file: test.csv')
        self.assertDictEqual(Statistic(dataset, 'Программист').salary,
                             {2020: 10759, 2021: 210000, 2022: 209608})
        self.assertDictEqual(Statistic(dataset, 'Программист').count,
                             {2020: 1, 2021: 1, 2022: 3})
        self.assertDictEqual(Statistic(dataset, 'Программист').city_perc,
                             {'Москва': 0.4, 'Минск': 0.4, 'Санкт-Петербург': 0.2})
