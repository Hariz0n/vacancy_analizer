import numpy as np


class Salary:
    """Класс, описывающий зарплату"""
    _currency_to_rub = {
        "AZN": 35.68, "BYR": 23.91, "EUR": 59.90,
        "GEL": 21.74, "KGS": 0.76, "KZT": 0.13,
        "RUR": 1, "UAH": 1.64, "USD": 60.66,
        "UZS": 0.0055,
    }

    def __init__(self, salary_from: float, salary_to: float, salary_gross: bool, salary_currency: str):
        """Инициализирует объект Salary, вычисляет среднюю зарплату

        :param salary_from: Нижняя вилка оклада
        :type salary_from: int
        :param salary_to: Нижняя вилка оклада
        :type salary_to: int
        :param salary_gross: Был ли произведен вычет налогов
        :type salary_gross: bool
        :param salary_currency: Валюта
        :type salary_currency: str
        """
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency
        if not np.isnan(self.salary_from) and not np.isnan(self.salary_to):
            self.salary_average = int((self.salary_from + self.salary_to) / 2)
        elif not np.isnan(self.salary_from):
            self.salary_average = int(salary_from)
        elif not np.isnan(self.salary_to):
            self.salary_average = int(salary_to)

    def get_average_salary_rub(self):
        """ Метод конвертации среднее зарплаты в рубли

        :return: Среднюю зарплату в рублях c учетом валюты
        :rtype: float
        """
        return self.salary_average * self._currency_to_rub[self.salary_currency]
