import os
from Report import Report
from Statistics import Statistic
from Table import Table
from csv_splitter import csv_splitter

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
    """ Класс-интерфейс для сбора вводимой информации пользователем для последующего использования"""

    def __init__(self):
        """Инициализирует объект класса InputConnect"""
        # selection = input('Вакансии или Статистика: ').strip()
        selection = 'Статистика'
        if selection == "Вакансии".strip():
            self.print_vacs()
        elif selection == "Статистика":
            self.get_stats()

    def get_stats(self):
        folder = 'vby'
        work_name = 'аналитик'
        folder = input('Введите название папки с csv файлами: ').strip()
        work_name = input('Введите название профессии: ').strip()
        csv_splitter(folder + '.csv') if not os.path.exists(folder) else None
        stats = Statistic(folder, work_name)
        stats.get_statistics()
        stats.get_city_stats()
        stats.print_statistic()
        report = Report(stats)
        report.generate_excel()
        report.generate_image()
        report.generate_pdf()

    def print_vacs(self):
        file_name = input('Введите название файла: ').strip()
        filter_data = list(filter(lambda e: e != "", input('Введите параметр фильтрации: ').split(': ')))
        sort_key = input('Введите параметр сортировки: ').strip()
        is_reversed_sort = True if input('Обратный порядок сортировки (Да / Нет): ').strip() == 'Да' else False
        table_ranges = list(map(int, input('Введите диапазон вывода: ').split()))
        fields = list(filter(lambda e: e != "", input('Введите требуемые столбцы: ').split(', ')))
        translation: dict[str, str] = russian
        if self.is_valid(table={
            'file_name': file_name,
            'filter_data': filter_data,
            'sort_key': sort_key,
            'is_reversed_sort': is_reversed_sort,
            'table_ranges': table_ranges,
            'fields': fields,
            'translation': translation
        }):
            table = Table(file_name.replace('.csv', ''), filter_data, sort_key, is_reversed_sort,
                          table_ranges, fields, translation)
            table.filter_vacancies()
            table.sort_vacancies()
            table.print_table()

    def is_valid(self, table: dict) -> bool:
        """Проверяет валидность введенных данных

        :param table: Проверка на тип выводимой информации
        :return: Валидны ли значения
        :rtype: bool
        """
        if not os.path.exists(table['file_name']):
            print("Файла не существует")
            return False
        if os.stat(table['file_name']).st_size == 0:
            print("Пустой файл")
            return False
        if len(table['filter_data']) == 1:
            print('Формат ввода некорректен')
            return False
        if len(table['filter_data']) and not table['filter_data'][0] in table['translation'].values():
            print('Параметр поиска некорректен')
            return False
        if table['sort_key'] and table['sort_key'] not in table['translation'].values():
            print('Параметр сортировки некорректен')
            return False
        if table['is_reversed_sort'] and table['is_reversed_sort'] != 'Да' and table['is_reversed_sort'] != 'Нет':
            print('Порядок сортировки задан некорректно')
            return False
        return True
