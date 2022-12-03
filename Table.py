import re
from datetime import datetime
from prettytable import PrettyTable, ALL
from DataSet import DataSet
from Vacancy import Vacancy


class Table:
    """Класс для обработки датасета и вывода данных в виде таблицы

    Attributes:
        file_name (str): Название файла
        filter_data (list(str, str)): Список с фильтруемым параметром и его значением
        sort_key (str): Параметр сортировки
        is_reversed_sort (bool): Обратная ли сортировка
        table_ranges list(int, int): Диапазон вывода строк таблицы
        fields list(str): Необходимые для вывода столбцы
        __translation dict(str, str): Словарь перевода
        __reversed_translation dict(str, str): Обратный словарь для перевода
        dataset (DataSet): Датасет вакансий
    """
    def __init__(self, file_name, filter_data, sort_key, is_reversed_sort, table_ranges, fields, translation):
        """ Создает объект Table

        :param file_name: Название файла
        :type file_name: str
        :param filter_data: Список с фильтруемым параметром и его значением
        :type filter_data: list[str, str]
        :param sort_key: Параметр сортировки
        :type sort_key: str
        :param is_reversed_sort: Обратная ли сортировка
        :type is_reversed_sort: bool
        :param table_ranges: Диапазон вывода строк таблицы
        :type table_ranges: list[int]
        :param fields: Необходимые для вывода столбцы
        :type fields: list[str]
        :param translation: Словарь перевода
        :type translation: dict[str, str]
        """
        self.file_name = file_name
        self.filter_data = filter_data
        self.sort_key = sort_key
        self.is_reversed_sort = is_reversed_sort
        self.table_ranges = table_ranges
        self.fields = fields
        self.__translation: dict[str, str] = translation
        self.__reversed_translation = dict([(v, k) for k, v in self.__translation.items()])
        self.dataset = DataSet(self.file_name)

    def filter_vacancies(self):
        """
        Фильтрует вакансии по заданному критерию
        :return: None
        """
        if not len(self.filter_data):
            return
        filtered: list[Vacancy] = []
        for vac in self.dataset.vacancies_objects:
            if self.__reversed_translation[self.filter_data[0]].startswith('salary_'):
                vacancy_filter_value = getattr(vac.salary,
                                               self.__reversed_translation[self.filter_data[0]])
            else:
                vacancy_filter_value = getattr(vac, self.__reversed_translation[self.filter_data[0]])
            if self.filter_data[0] == self.__translation['key_skills']:
                if not all([k in vacancy_filter_value for k in self.filter_data[1].split(', ')]):
                    continue
            elif self.filter_data[0] == self.__translation['salary']:
                int_value = int(float(self.filter_data[1]))
                if vac.salary.salary_from > int_value or int_value > vac.salary.salary_to:
                    continue
            elif self.filter_data[0] == self.__translation['published_at']:
                if ".".join(vac.published_at[:10].split('-')[::-1]) != self.filter_data[1]:
                    continue
            elif self.filter_data[1] in self.__reversed_translation:
                if vacancy_filter_value != self.__reversed_translation[self.filter_data[1]]:
                    continue
            elif vacancy_filter_value != self.filter_data[1]:
                continue
            filtered.append(vac)
        if not filtered:
            print('Ничего не найдено')
        self.dataset.vacancies_objects = filtered

    def sort_vacancies(self):
        """
        Сортирует вакансии по заданному критерию
        :return:
        """
        if not self.sort_key and self.dataset.vacancies_objects:
            return
        is_reversed = True if self.is_reversed_sort == 'Да' else False
        if self.sort_key == self.__translation['key_skills']:
            def sort_func(vac: Vacancy):
                return len(vac.key_skills)
        elif self.sort_key == self.__translation['experience_id']:
            def sort_func(vac: Vacancy):
                return re.sub(r'\D', '', vac.experience_id)
        elif self.sort_key == self.__translation['salary']:
            def sort_func(vac: Vacancy):
                return vac.salary.convert_currency_average()
        elif self.sort_key == self.__translation['published_at']:
            def sort_func(vac):
                return datetime.strptime(getattr(vac, 'published_at'),
                                         "%Y-%m-%dT%H:%M:%S%z")
        else:
            def sort_func(vac):
                return getattr(vac, self.__reversed_translation[self.sort_key])
        self.dataset.vacancies_objects.sort(key=sort_func, reverse=is_reversed)

    def print_table(self):
        """
        Выводит таблицу с конечными с отфильтрованными и отсортированными данными
        :return: None
        """
        if not self.dataset.vacancies_objects:
            return
        table = PrettyTable()
        table.hrules = ALL
        table.align = 'l'
        table.field_names = ['№', *[self.__translation[k] for k in self.dataset.vacancies_objects[0].__dict__.keys()]]
        table._max_width = {i: 20 for i in table.field_names}
        c = 1
        nl = '\n'

        for vacancy in self.dataset.vacancies_objects:
            row = [c]
            for header, value in vacancy.__dict__.items():
                if header == 'key_skills':
                    row_value = nl.join(value)
                    row.append(f"{row_value[:100]}{'...' if len(row_value) > 100 else ''}")
                elif header == 'published_at':
                    row.append(".".join(value[:10].split('-')[::-1]))
                elif header == 'salary':
                    row.append(
                        f'{"{:,}".format(value.salary_from).replace(",", " ")} - '
                        f'{"{:,}".format(value.salary_to).replace(",", " ")} '
                        f'({self.__translation[value.salary_currency]}) '
                        f'({"Без вычета налогов" if value.salary_gross == "True" else "С вычетом налогов"})')
                else:
                    row_value = value
                    row.append(self.__translation[value] if value in self.__translation
                               else f"{row_value[:100]}{'...' if len(row_value) > 100 else ''}")
            table.add_row(row)
            c += 1

        if len(self.table_ranges) == 0:
            self.table_ranges.append(1)
            self.table_ranges.append(table.rowcount + 1)
        elif len(self.table_ranges) == 1:
            self.table_ranges.append(table.rowcount + 1)

        print(table.get_string(start=self.table_ranges[0] - 1, end=self.table_ranges[1] - 1,
                               fields=['№', *self.fields] if len(self.fields) > 0 else table.field_names))
