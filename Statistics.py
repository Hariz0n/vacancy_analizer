from DataSet import DataSet
from pandas import DataFrame, concat
import os
import multiprocessing as mp

class Statistic:
    data: DataFrame
    def __init__(self, folder: str, work_name: str):
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
        self.work_name: str = work_name
        self.folder: str = folder


    def getData(self):
        """
        Метод получения датафлейма с вакансиями
        :return: Датафрейм с вакансиями
        """
        paths = list(map(lambda e: f"{self.folder}/{e}",os.listdir(self.folder)))
        print(self.folder, paths)
        with mp.Pool() as pl:
            self.data = concat(list(map(lambda e: e.vacs_list, pl.map(DataSet, paths))))

    def getStatistics(self):
        if self.data is None:
            return
        self.salary_mean = self.data.groupby(self.data['published_at'].map(lambda x: x.year))['salary'].mean().astype(int).to_dict()
        self.count = self.data.groupby(self.data['published_at'].map(lambda x: x.year))['name'].count().to_dict()
        worker = self.data[self.data['name'].str.contains(self.work_name, case=False)]
        self.worker_mean = worker.groupby(worker['published_at'].map(lambda x: x.year))['salary'].mean().astype(int).to_dict()
        self.worker_count = worker.groupby(worker['published_at'].map(lambda x: x.year))['name'].count().to_dict()
        self.city_salary = {}
        self.city_perc = {}

    def print_statistic(self):
        """Метод вывода статистики в консоль

        :return: Статистику в консоль
        """
        print(f"Динамика уровня зарплат по годам: {self.salary_mean}")
        print(f"Динамика количества вакансий по годам: {self.count}")
        print(f"Динамика уровня зарплат по годам для выбранной профессии: {self.worker_mean}")
        print(f"Динамика количества вакансий по годам для выбранной профессии: {self.worker_count}")
        print(f"Уровень зарплат по городам (в порядке убывания): {dict()}")
        print(f"Доля вакансий по городам (в порядке убывания): {dict()}")
