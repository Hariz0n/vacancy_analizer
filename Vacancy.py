from datetime import datetime
from Salary import Salary


class Vacancy:
    """Класс для вакансий"""

    def __init__(self, name: str, salary: int, area_name: str, published_at: datetime):
        """ Создает инстанс объекта Vacancy

        :param name: Название вакансии
        :param area_name: Город
        :param published_at: Дата публикации
        :param salary: Зарплата
        """
        self.name: str = name
        self.salary: int = salary
        self.area_name: str = area_name
        self.published_at: datetime = published_at

    def __str__(self):
        """ Текстовое представление объекта Vacancy
        :return: Информацию о вакансии
        """
        return f'Вакансия: {self.name}\n' \
               f'Зарплата: {self.salary if self.salary else "Нет данных"}\n' \
               f'Город: {self.area_name if self.area_name else "Нет данных"}\n' \
               f'Дата публикации: {self.published_at.strftime("%d %b %Y | %I:%M %p") if self.published_at else "Нет данных"}\n'
