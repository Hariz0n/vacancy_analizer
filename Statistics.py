import pandas

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
        print(self.folder, paths)
        with mp.Pool() as pl:
            self.data = concat(list(map(lambda e: e.vacs_list, pl.map(DataSet, paths))))
            db.addData(self.data, 'vacancies')

    def getStatistics(self):
        """
        Метод анализа данных. Сохраняется статистику в инстанс класса
        :return: словари статистик
        """
        if self.data is None:
            return
        self.salary_mean = self.data.groupby(self.data['published_at'].map(lambda x: x.year))['salary'].mean().astype(int).to_dict()
        self.count = self.data.groupby(self.data['published_at'].map(lambda x: x.year))['name'].count().to_dict()
        worker = self.data[self.data['name'].str.contains(self.work_name, case=False)]
        self.worker_mean = worker.groupby(worker['published_at'].map(lambda x: x.year))['salary'].mean().astype(int).to_dict()
        self.worker_count = worker.groupby(worker['published_at'].map(lambda x: x.year))['name'].count().to_dict()
        area = self.data[self.data['area_name'].map((self.data['area_name'].value_counts() / len(self.data))*100) > 1]
        self.city_salary = area.groupby(area['area_name'])['salary'].mean().sort_values(ascending=False).head(10).to_dict()
        self.city_perc = (area.groupby(area['area_name'])['salary'].count() / len(self.data)).sort_values(ascending=False).head(10).to_dict()
        worker_area = worker[worker['area_name'] == self.area]
        self.worker_area_mean = worker_area.groupby(worker_area['published_at'].map(lambda x: x.year))['salary'].mean().astype(int).to_dict()
        self.worker_area_count = worker_area.groupby(worker_area['published_at'].map(lambda x: x.year))['name'].count().to_dict()

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
        print(f"Динамика уровня зарплат по годам для выбранной профессии и региона: {self.worker_area_mean}")
        print(f"Динамика количества вакансий по годам для выбранной профессии и региона: {self.worker_area_count}")
