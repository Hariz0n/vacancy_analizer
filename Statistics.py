from DataSet import DataSet


class Statistic:
    """
    Класс для сбора статистики о вакансиях

    Attributes:
        city_perc (dict(str, int)): Словарь с информацией долях вакансий по городам
        salary_city (dict(str, int)): Словарь с информацией о уровнях зарплат по городам
        count_worker (dict(str, int)): Словарь с динамикой количества вакансий по годам для выбранной профессии
        salary_worker (dict(str, int)): Словарь с динамикой уровня зарплат по годам для выбранной профессии
        count (dict(str, int)): Словарь с динамикой количества вакансий по годам
        salary (dict(str, int)): Словарь с динамикой уровня зарплат по годам
        statistic (dict(str, dict)): Словарь со всей необработанной статистикой
        dataset (DataSet): Датасет вакансий
        work_name (str): Название профессии
    """
    def __init__(self, dataset: DataSet, work_name: str):
        """ Инициализирует объект Statistic

        :param dataset: Датасет вакансий
        :type dataset: DataSet
        :param work_name: Название профессии
        :type work_name: str
        """
        self.city_perc = None
        self.salary_city = None
        self.count_worker = None
        self.salary_worker = None
        self.count = None
        self.salary = None
        self.statistic: dict[str, dict] = None
        self.dataset: DataSet = dataset
        self.work_name = work_name
        self.get_statistics()

    def get_statistics(self):
        total: dict[int, list[int, int]] = {}
        work: dict[int, list[int, int]] = {}
        city: dict[str, list[int, int]] = {}

        for vacancy in self.dataset.vacancies_objects:
            date = int(vacancy.published_at[:4])
            if date not in total:
                total[date] = [0, 0]
                work[date] = [0, 0]
            if vacancy.area_name not in city:
                city[vacancy.area_name] = [0, 0]
            if self.work_name in vacancy.name:
                if date not in work:
                    work[date] = [0, 0]
                work[date][0] += vacancy.salary.convert_currency_average()
                work[date][1] += 1
            total[date][0] += vacancy.salary.convert_currency_average()
            total[date][1] += 1
            city[vacancy.area_name][0] += vacancy.salary.convert_currency_average()
            city[vacancy.area_name][1] += 1

        self.statistic = {'total': total, 'work': work, 'city': city}
        self.format()

    def format(self):
        self.salary = dict(sorted([(k, int(v[0] / (v[1] or 1))) for k, v in self.statistic['total'].items()]))
        self.count = dict(sorted([(k, v[1]) for k, v in self.statistic['total'].items()]))
        self.salary_worker = dict(sorted([(k, int(v[0] / (v[1] or 1))) for k, v in self.statistic['work'].items()]))
        self.count_worker = dict(sorted([(k, v[1]) for k, v in self.statistic['work'].items()]))
        filtered_cities = dict([(k, v) for k, v in self.statistic['city'].items()
                                if int((v[1] / len(self.dataset.vacancies_objects)) * 100) >= 1])
        self.salary_city = dict(sorted([(k, int(v[0] / v[1])) for k, v in filtered_cities.items()],
                                       key=lambda e: -e[1])[:10])
        self.city_perc = dict(sorted([(k, round(v[1] / len(self.dataset.vacancies_objects), 4))
                                      for k, v in filtered_cities.items()], key=lambda e: -e[1])[:10])

    def print_statistic(self):
        print(f"Динамика уровня зарплат по годам: {self.salary}")
        print(f"Динамика количества вакансий по годам: {self.count}")
        print(f"Динамика уровня зарплат по годам для выбранной профессии: {self.salary_worker}")
        print(f"Динамика количества вакансий по годам для выбранной профессии: {self.count_worker}")
        print(f"Уровень зарплат по городам (в порядке убывания): {self.salary_city}")
        print(f"Доля вакансий по городам (в порядке убывания): {self.city_perc}")