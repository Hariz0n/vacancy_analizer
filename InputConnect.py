import os
import pandas as pd
from Report import Report
from Statistics import Statistic

russian = {
    "name": "Название",
    "description": "Описание",
    "key_skills": "Навыки",
    "experience_id": "Опыт работы",
    "premium": "Премиум-вакансия",
    "employer_name": "Компания",
    "salary_from": "Нижняя граница вилки оклада",
    "salary_to": "Верхняя граница вилки оклада",
    "salary_gross": "Оклад указан до вычета налогов",
    "salary_currency": "Идентификатор валюты оклада",
    "salary": "Оклад",
    "salary_average": "Средняя зарплата",
    "area_name": "Название региона",
    "published_at": "Дата публикации вакансии",
    "noExperience": "Нет опыта",
    "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет",
    "moreThan6": "Более 6 лет",
    "AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум",
    "True": "Да",
    "False": "Нет",
}


class InputConnect:
    """ Класс-интерфейс для сбора вводимой информации пользователем для последующего использования"""

    def __init__(self):
        """Инициализирует объект класса InputConnect"""
        while True:
            # file_name = input('Введите название файла: ')
            file_name = 'vacancies_dif_currencies.csv'
            if os.path.exists(file_name) and os.path.splitext(file_name)[1] == '.csv':
                self.fileName, self.fileExtension = os.path.splitext(file_name)
                break
            print('Введено неверное название файла! Попробуйте снова')
        self.work_name = 'аналитик'
        # self.work_name = input('Введите название профессии: ')
        self.get_stats()


    def get_stats(self):
        InputConnect.csv_splitter(self.fileName + self.fileExtension) \
            if not os.path.exists(self.fileName) else None
        stats = Statistic(self.fileName, self.work_name)
        stats.getData()
        stats.getStatistics()
        stats.print_statistic()
        report = Report(stats)
        report.generate_excel()
        report.generate_image()
        report.generate_pdf()

    @staticmethod
    def csv_splitter(file_name: str):
        """
        Разделяет переданный csv файл по годам
        :return: None
        """
        data = pd.read_csv(file_name, index_col=0, engine="pyarrow")
        name = file_name.replace('.csv', '')
        years = data['published_at'].dt.year.unique()
        os.makedirs(name, exist_ok=True)
        for year in [y for y in years if y is not None]:
            if not year:
                continue
            data[data['published_at'].dt.year == year].to_csv(f'{name}/{year}.csv')



