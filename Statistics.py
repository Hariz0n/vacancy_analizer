import pandas as pd
from DataSet import DataSet
from pandas import DataFrame, concat
import os
import multiprocessing as mp
from db import DB
db = DB()
class Statistic:
    data: DataFrame
    def __init__(self, folder: str, work_name: str, area: str):
        """Создает инстанс объекта Statistics

        :param folder: Название папки с csv файлами
        :param work_name: Название профессии
        """

        self.salary_mean: dict = None
        self.count: dict = None
        self.worker_mean: dict = None
        self.worker_count: dict = None
        self.city_salary: dict = None
        self.city_perc: dict = None
        self.worker_area_mean: dict = None
        self.worker_area_count: dict = None
        self.work_name: str = work_name
        self.folder: str = folder
        self.area: str = area


    def getData(self):
        """
        Метод получения датафлейма с вакансиями
        :return: Датафрейм с вакансиями
        """
        paths = list(map(lambda e: f"{self.folder}/{e}",os.listdir(self.folder)))
        # print(self.folder, paths)
        with mp.Pool() as pl:
            self.data = concat(list(map(lambda e: e.vacs_list, pl.map(DataSet, paths))))
            db.addVacanciesData(self.data, 'vacancies')

    def getStatistics(self):
        """
        Метод анализа данных. Сохраняется статистику в инстанс класса
        :return: словари статистик
        """
        database = DB()
        if self.data is None:
            return
        self.salary_mean = pd.read_sql(f"SELECT strftime('%Y', published_at) date, CAST(round(avg(salary)) as int) salary "
                                 f"FROM vacancies "
                                 f"GROUP BY date", database.con, index_col='date')['salary'].to_dict()
        self.count = pd.read_sql(f"SELECT strftime('%Y', published_at) date, count(*) count "
                                 f"FROM vacancies "
                                 f"GROUP BY date", database.con, index_col='date')['count'].to_dict()
        self.worker_mean = pd.read_sql(f"SELECT strftime('%Y', published_at) date, CAST(round(avg(salary)) as int) salary "
                                       f"FROM vacancies WHERE lower(name) like '%{self.work_name}%' "
                                       f"GROUP BY date", database.con, index_col='date')['salary'].to_dict()
        self.worker_count = pd.read_sql(f"SELECT strftime('%Y', published_at) date, count(*) count "
                                        f"FROM vacancies WHERE lower(name) like '%{self.work_name}%' "
                                        f"GROUP BY date", database.con, index_col='date')['count'].to_dict()
        self.city_salary = pd.read_sql("WITH percs AS ("
                                       "SELECT area_name area, round(count(*)*1.0 / sum(count(*)) over(), 3) perc, CAST(avg(salary) as int) salary "
                                       "FROM vacancies GROUP BY area_name) "
                                       "SELECT area, salary FROM percs "
                                       "WHERE percs.perc > 0.01 "
                                       "ORDER BY salary DESC LIMIT 10", database.con, index_col='area')['salary'].to_dict()
        self.city_perc = pd.read_sql("WITH percs AS ("
                                     "SELECT area_name area, round(count(*)*1.0 / sum(count(*)) over(), 3) perc "
                                     "FROM vacancies GROUP BY area_name) "
                                     "SELECT * FROM percs "
                                     "WHERE percs.perc > 0.01 "
                                     "ORDER BY perc DESC LIMIT 10", database.con, index_col='area')['perc'].to_dict()

        worker_area = self.data[(self.data['area_name'] == self.area) & (self.data['name'].str.contains(self.work_name, case=False))]
        self.worker_area_mean = worker_area.groupby(worker_area['published_at'].map(lambda x: x.year))[
            'salary'].mean().astype(int).to_dict()
        self.worker_area_count = worker_area.groupby(worker_area['published_at'].map(lambda x: x.year))[
            'name'].count().to_dict()

    def print_statistic(self):
        """Метод вывода статистики в консоль

        :return: Статистику в консоль
        """
        print(f"Динамика уровня зарплат по годам: {self.salary_mean}")
        print(f"Динамика количества вакансий по годам: {self.count}", end='\n\n')
        print(f"Динамика уровня зарплат по годам для выбранной профессии: {self.worker_mean}")
        print(f"Динамика количества вакансий по годам для выбранной профессии: {self.worker_count}", end='\n\n')
        print(f"Уровень зарплат по городам (в порядке убывания): {self.city_salary}")
        print(f"Доля вакансий по городам (в порядке убывания): {self.city_perc}", end='\n\n')
        print(f"Из прошлого задания (3.4.3):\n")
        print(f"Динамика уровня зарплат по годам для выбранной профессии и региона: {self.worker_area_mean}")
        print(f"Динамика количества вакансий по годам для выбранной профессии и региона: {self.worker_area_count}")
