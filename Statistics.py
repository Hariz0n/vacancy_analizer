from DataSet import DataSet
import os
import multiprocessing as mp


class Statistic:
    def __init__(self, folder: str, work_name: str):
        """Создает инстанс объекта Statistics

        :param folder: Название папки с csv файлами
        :param work_name: Название профессии
        """
        self.work_name: str = work_name
        self.folder = folder
        self.datasets: list[DataSet] = []
        self.main_dataset: DataSet = None
        self.salary_by_year: dict[int, int] = {}
        self.count_by_year: dict[int, int] = {}
        self.work_salary_by_year: dict[int, int] = {}
        self.work_count_by_year: dict[int, int] = {}
        self.city_salary_by_year: dict[str, int] = {}
        self.city_rate_by_year: dict[str, float] = {}

    def _get_stats_from_csv(self, dataset: DataSet):
        """Собирает информацию о вакансиях и о преданной профессии

        :param dataset: csv Датасет
        :return: Кортеж с данными об общей зарплате и зарплате по профессии
        """
        dataset.csv_parser()
        total = {}
        work = {}
        for vac in dataset.vacs_list:
            year = vac.published_at.year
            if vac.published_at.year not in total:
                total[year] = [0, 0]
                work[year] = [0, 0]
            if self.work_name in vac.name:
                work[year][0] += vac.salary.get_average_salary_rub()
                work[year][1] += 1
            total[year][0] += vac.salary.get_average_salary_rub()
            total[year][1] += 1
        return total, work

    def get_statistics_async(self):
        """Метод получения статистики асинхронно

        :return: None
        """
        for csv_file in os.listdir(self.folder):
            self.datasets.append(DataSet(f"{self.folder}/{csv_file.replace('.csv', '')}"))
        with mp.Pool() as pl:
            stats = pl.map(self._get_stats_from_csv, self.datasets)
        data = {"total": {}, "work": {}}
        for t, w in stats:
            data["total"].update(t)
            data["work"].update(w)
        self.salary_by_year, self.work_salary_by_year, self.count_by_year, self.work_count_by_year = \
            self.format_salary_count(data)

    def get_statistics(self):
        """Метод получения статистики синхронно

        :return: None
        """
        if not self.main_dataset:
            self.main_dataset = DataSet(self.folder)
            self.main_dataset.csv_parser()
        data = {"total": {}, "work": {}}
        result = self._get_stats_from_csv(self.main_dataset)
        data["total"].update(result[0])
        data["work"].update(result[1])
        self.salary_by_year, self.work_salary_by_year, self.count_by_year, self.work_count_by_year = \
            self.format_salary_count(data)

    def get_city_stats(self):
        """Метод получения статистики по городам

        :return: None
        """
        city_data = {}
        if not self.main_dataset:
            self.main_dataset = DataSet(self.folder)
            self.main_dataset.csv_parser()
        for vac in self.main_dataset.vacs_list:
            if vac.area_name not in city_data:
                city_data[vac.area_name] = [0, 0]
            city_data[vac.area_name][0] += vac.salary.get_average_salary_rub()
            city_data[vac.area_name][1] += 1
        self.city_salary_by_year, self.city_rate_by_year = self.format_city(city_data)

    def format_salary_count(self, stats: dict):
        """Метод форматирования статистики зарплат

        :param stats: Неотформотированная статистика
        :return: Отформатированную статистику зарплат и количества вакансий
        """
        salary = dict(sorted([(k, int(v[0] / (v[1] or 1))) for k, v in stats['total'].items()]))
        count = dict(sorted([(k, v[1]) for k, v in stats['total'].items()]))
        salary_worker = dict(
            sorted([(k, int(v[0] / (v[1] or 1))) for k, v in stats['work'].items()]))
        count_worker = dict(sorted([(k, v[1]) for k, v in stats['work'].items()]))
        return salary, salary_worker, count, count_worker

    def format_city(self, stats: dict):
        """Метод форматирования статистики городов

        :param stats: Неотформотированная статистика
        :return: Отформатированную статистику городов
        """
        filtered_cities = dict([(k, v) for k, v in stats.items()
                                if int((v[1] / len(self.main_dataset.vacs_list)) * 100) >= 1])
        salary_city = dict(sorted([(k, int(v[0] / v[1])) for k, v in filtered_cities.items()],
                                  key=lambda e: -e[1])[:10])
        city_perc = dict(sorted([(k, round(v[1] / len(self.main_dataset.vacs_list), 4))
                                 for k, v in filtered_cities.items()], key=lambda e: -e[1])[:10])
        return salary_city, city_perc

    def print_statistic(self):
        """Метод вывода статистики в консоль

        :return: Статистику в консоль
        """
        print(f"Динамика уровня зарплат по годам: {self.salary_by_year}")
        print(f"Динамика количества вакансий по годам: {self.count_by_year}")
        print(f"Динамика уровня зарплат по годам для выбранной профессии: {self.work_salary_by_year}")
        print(f"Динамика количества вакансий по годам для выбранной профессии: {self.work_count_by_year}")
        print(f"Уровень зарплат по городам (в порядке убывания): {self.city_salary_by_year}")
        print(f"Доля вакансий по городам (в порядке убывания): {self.city_rate_by_year}")
