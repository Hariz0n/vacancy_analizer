from Salary import Salary


class Vacancy:
    name: str = None
    description: int = None
    key_skills: list = None
    experience_id: str = None
    premium: str = None
    employer_name: str = None
    salary: Salary = None
    area_name: str = None
    published_at: str = None

    def __init__(self, values: dict, salary: Salary):
        for key in values:
            if key == 'area_name':  # Вставляет пол
                self.salary: Salary = salary
            setattr(self, key, values[key])

