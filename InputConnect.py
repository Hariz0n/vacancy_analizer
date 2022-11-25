import os

from DataSet import DataSet
from Report import Report
from Statistics import Statistic
from Table import Table

russian = {
    "name": "Название",
    "description": "Описание",
    "key_skills": "Навыки",
    "experience_id": "Опыт работы",
    "premium": "Премиум-вакансия",
    "employer_name": "Компания",
    "salary_from": "Нижняя граница вилки оклада",
    "salary_to": "Верхняя граница вилки оклада",
    "salary_gross": "Оклад указан до вычета налогов",
    "salary_currency": "Идентификатор валюты оклада",
    "salary": "Оклад",
    "salary_average": "Средняя зарплата",
    "area_name": "Название региона",
    "published_at": "Дата публикации вакансии",
    "noExperience": "Нет опыта",
    "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет",
    "moreThan6": "Более 6 лет",
    "AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум",
    "True": "Да",
    "False": "Нет",
}

class InputConnect:
    def __init__(self):
        selection = input('Вакансии или Статистика: ').strip()
        if selection == "Вакансии":
            self.file_name = input('Введите название файла: ').strip()
            self.filter_data = list(filter(lambda e: e != "", input('Введите параметр фильтрации: ').split(': ')))
            self.sort_key = input('Введите параметр сортировки: ').strip()
            self.is_reversed_sort = input('Обратный порядок сортировки (Да / Нет): ').strip()
            self.table_ranges = list(map(int, input('Введите диапазон вывода: ').split()))
            self.fields = list(filter(lambda e: e != "", input('Введите требуемые столбцы: ').split(', ')))
            self.__translation: dict[str, str] = russian
            if self.is_valid(True):
                self.table = Table(self.file_name, self.filter_data, self.sort_key, self.is_reversed_sort,
                                   self.table_ranges, self.fields, russian)
                self.table.filter_vacancies()
                self.table.sort_vacancies()
                self.table.print_table()
        elif selection == "Статистика":
            self.file_name = input('Введите название файла: ').strip()
            self.work_name = input('Введите название профессии: ').strip()
            if self.is_valid():
                dataset: DataSet = DataSet(self.file_name)
                stats = Statistic(dataset, self.work_name)
                stats.print_statistic()
                report = Report(stats)
                report.generate_excel()
                report.generate_image()
                report.generate_pdf()

    def is_valid(self, isTable=False) -> bool:
        if os.stat(self.file_name).st_size == 0:
            print("Пустой файл")
            return False
        if isTable:
            if len(self.filter_data) == 1:
                print('Формат ввода некорректен')
                return False
            elif len(self.filter_data) and not self.filter_data[0] in self.__translation.values():
                print('Параметр поиска некорректен')
                return False
            elif self.sort_key and self.sort_key not in self.__translation.values():
                print('Параметр сортировки некорректен')
                return False
            elif self.is_reversed_sort and self.is_reversed_sort != 'Да' and self.is_reversed_sort != 'Нет':
                print('Порядок сортировки задан некорректно')
                return False
        return True

    