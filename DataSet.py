from Vacancy import Vacancy
from pandas import read_csv, DataFrame, isnull

currencies = read_csv('curs.csv', engine='pyarrow', index_col=0)


class DataSet:
    """Класс представляющий датасет вакансий HH.ru"""

    def __init__(self, path: str):
        """Создает инстанс класса DataSet

        :param path: Название папки с csv файлами и одновременно название csv файла без расширения
        """
        self.file_path: str = path
        self.vacs_list: DataFrame = self.csv_parser()

    def csv_parser(self):
        """Метод парсинга CSV файлов"""

        data = read_csv(self.file_path, engine="pyarrow")
        data['salary'] = data.apply(DataSet.get_salary, axis=1)
        data = data[['name', 'salary', 'area_name', 'published_at']]
        return data

    @staticmethod
    def get_salary(row):
        """
        Метод получения значений столбца Salary на основе столбцов Salary_from, salary_to, salary_currency
        :param row: строка датафрейма Pandas
        :return: значение ячейки
        """
        if not isnull(row['salary_from']) and not isnull(row['salary_to']):
            salary = int((row['salary_from'] + row['salary_to']) / 2)
        elif not isnull(row['salary_from']):
            salary = row['salary_from']
        elif not isnull(row['salary_to']):
            salary = row['salary_to']
        else:
            salary = None

        if salary is None or row['salary_currency'] == 'RUR' or \
                row['salary_currency'] not in currencies.columns or \
                isnull(currencies.loc[row['published_at'].strftime('%Y-%m')][row['salary_currency']]):
            return salary
        return int(salary * currencies.loc[row['published_at'].strftime('%Y-%m')][row['salary_currency']])
