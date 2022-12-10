from Vacancy import Vacancy
from Salary import Salary
import pandas as pd


class DataSet:
    """Класс представляющий датасет вакансий HH.ru"""
    _valid_columns = ["name",
                      "description",
                      "key_skills",
                      "experience_id",
                      "premium",
                      "employer_name",
                      "salary_from",
                      "salary_to",
                      "salary_gross",
                      "salary_currency",
                      "area_name",
                      "published_at"]

    def __init__(self, path: str):
        """Создает инстанс класса DataSet

        :param path: Название папки с csv файлами и одновременно название csv файла без расширения
        """
        self.path: str = path
        self.vacs_list: list[Vacancy] = []

    def csv_parser(self, file=None):
        """Метод парсинга CSV файлов"""

        if self.vacs_list:
            print('Данные уже обработаны')
            return

        table = pd.read_csv(file if file else f'{self.path}.csv', engine="pyarrow").dropna()
        if 'key_skills' in table.columns:
            table['key_skills'] = table['key_skills'].str.split('\n')
        if 'description' in table.columns:
            table['description'] = table['description'].str.replace(r'<[^>]+>', '', regex=True) \
                .str.replace("\s+", " ", regex=True) \
                .str.split('\n| ', regex=True).str.join(' ')
        columns: list[str] = table.columns.to_list()
        for row in table.to_numpy():
            data = dict([(k, None) for k in self._valid_columns])
            for column in columns:
                try:
                    column_value = row.item(columns.index(column))
                except ValueError:
                    column_value = None
                data[column] = column_value

            self.vacs_list.append(Vacancy(data['name'], data['description'], data['key_skills'],
                                          data['experience_id'], data['premium'], data['employer_name'],
                                          data['area_name'], data['published_at'],
                                          Salary(data['salary_from'], data['salary_to'],
                                                 data['salary_gross'], data['salary_currency'])))
        if not self.vacs_list:
            print('Нет данных')

