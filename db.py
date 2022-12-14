import sqlite3
from threading import Lock
from pandas import DataFrame


class DB:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DB, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.con = sqlite3.connect('db.sqlite')
        self.cur = self.con.cursor()

    def addCurrenciesData(self, df: DataFrame, table_name: str):
        """Метод создания таблицы валют и добавления в нее данных
        :param df: ДадаФрейм с валютами
        :param table_name: название таблицы в БД
        :return: Ничего
        """
        df.to_sql(table_name, self.con, if_exists='replace', index_label='date')

    def addVacanciesData(self, df: DataFrame, table_name: str):
        """Метод создания таблицы вакансий и добавления в нее данных
        :param df: ДадаФрейм с вакансиями
        :param table_name: название таблицы в БД
        :return: Ничего
        """
        df.to_sql(table_name, self.con, if_exists='replace')