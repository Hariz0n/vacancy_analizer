from Salary import Salary


class Vacancy:
    """ Класс для вакансий

    Attributes:
        name (str): Название вакансии
        description (str): Описание вакансии
        key_skills (list(str)): Необходимые навыки
        experience_id (str): Опыт работы
        premium (str): Является ли вакансия премиум вакансией
        employer_name (str): Название компании
        salary (Salary): Объект Salary, содержащий информации о зарплате вакансии
        area_name (str): Город
        published_at (str): Дата публикации
    """
    name: str = None
    description: int = None
    key_skills: list[str] = None
    experience_id: str = None
    premium: str = None
    employer_name: str = None
    salary: Salary = None
    area_name: str = None
    published_at: str = None

    def __init__(self, values: dict, salary: Salary):
        """

        :param values: Cловарь с полями о вакансии
        :type values: dict
        :param salary: Объект Salary
        :type salary: Salary
        """
        for key in values:
            if key == 'area_name':  # Вставляет пол
                self.salary: Salary = salary
            setattr(self, key, values[key])

