from Vacancy import Vacancy
import pandas as pd

currencies = pd.read_csv('curs.csv', engine='pyarrow', index_col=0)


class DataSet:
    """Класс представляющий датасет вакансий HH.ru"""
    _valid_columns = ["name",
                      "salary_from",
                      "salary_to",
                      "salary_currency",
                      "area_name",
                      "published_at"]

    def __init__(self, path: str):
        """Создает инстанс класса DataSet

        :param path: Название папки с csv файлами и одновременно название csv файла без расширения
        """
        self.path: str = path
        self.vacs_list: list[Vacancy] = self.csv_parser()

    def csv_parser(self):
        """Метод парсинга CSV файлов"""

        data = pd.read_csv(self.path, engine="pyarrow")
        data['salary'] = data.apply(DataSet.get_salary, axis=1)
        data = data.drop(['salary_from', 'salary_to', 'salary_currency'], axis=1) \
            .reindex(columns=['name', 'salary', 'area_name', 'published_at'])

        data.head(100).to_csv('first-one-hundred-by-pandas.csv')

        return [Vacancy(name, salary, area_name, published_at) for name, salary, area_name, published_at in
                data.to_numpy()]

    @staticmethod
    def get_salary(row):
        if not pd.isnull(row['salary_from']) and not pd.isnull(row['salary_to']):
            salary = int((row['salary_from'] / row['salary_to']) / 2)
        elif not pd.isnull(row['salary_from']):
            salary = row['salary_from']
        elif not pd.isnull(row['salary_to']):
            salary = row['salary_to']
        else:
            salary = None
        if salary is None or row['salary_currency'] not in currencies.columns or \
                pd.isnull(currencies.loc[row['published_at'].strftime('%Y-%m')][row['salary_currency']]):
            return None
        else:
            return int(salary * currencies.loc[row['published_at'].strftime('%Y-%m')][row['salary_currency']])

test = DataSet('vacancies_dif_currencies.csv')
