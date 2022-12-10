from datetime import datetime
from Salary import Salary


class Vacancy:
    """Класс для вакансий"""

    def __init__(self, name: str, description: str, key_skills: list[str],
                 experience_id: str, premium: bool, employer_name: str,
                 area_name: str, published_at: datetime, salary: Salary):
        """ Создает инстанс объекта Vacancy

        :param name: Название вакансии
        :param description: Описание вакансии
        :param key_skills: Навыки
        :param experience_id: Опыт работы
        :param premium: Является ли премиум вакансией
        :param employer_name: Имя работодателя
        :param area_name: Город
        :param published_at: Дата публикации
        :param salary: Зарплата
        """
        self.name: str = name
        self.description: str = description
        self.key_skills: list[str] = key_skills
        self.experience_id: str = experience_id
        self.premium: bool = premium
        self.employer_name: str = employer_name
        self.salary: Salary = salary
        self.area_name: str = area_name
        self.published_at: datetime = published_at

    def __str__(self):
        """ Текстовое представление объекта Vacancy
        :return: Информацию о вакансии
        """
        return f'Вакансия: {self.name}\n' \
               f'Описание: {self.description[:100] if self.description else "Нет данных"}\n' \
               f'Навыки: {", ".join(self.key_skills[:3]) if self.key_skills else "Нет данных"}\n' \
               f'Опыт работы: {self.experience_id if self.experience_id else "Нет данных"}\n' \
               f'Премиум: {self.premium if self.premium else "Нет данных"}\n' \
               f'Название компании | работодателя: {self.employer_name if self.employer_name else "Нет данных"}\n' \
               f'Зарплата: {self.salary if self.salary else "Нет данных"}\n' \
               f'Город: {self.area_name if self.area_name else "Нет данных"}\n' \
               f'Город: {self.published_at.strftime("%d %b %Y | %I:%M %p") if self.published_at else "Нет данных"}\n'
