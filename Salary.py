class Salary:
    """ Класс, описывающий зарплату

    Attributes:
        salary_from (int): Нижняя вилка оклада
        salary_to (int): Верхняя вилка оклада
        salary_gross (str): Был ли произведен вычет налого из зарплаты
        salary_currency (str): Валюта
        salary_average (int): Средняя заплата
        _currency_to_rub: Словарь курсов валют относительно рубля
    """
    salary_from: int = None
    salary_to: int = None
    salary_gross: str = None
    salary_currency: str = None
    salary_average: int = None
    _currency_to_rub = {
        "AZN": 35.68, "BYR": 23.91, "EUR": 59.90,
        "GEL": 21.74, "KGS": 0.76, "KZT": 0.13,
        "RUR": 1, "UAH": 1.64, "USD": 60.66,
        "UZS": 0.0055,
    }

    def __init__(self, salary: dict):
        """Инициализирует объект Salary, вычисляет среднюю зарплату

        :param dict salary: Словарь содержащий поля salaru_* - from, to, gross, currency

        >>> Salary({"salary_from": 1000,"salary_to": 5000,"salary_gross": 'False',"salary_currency": "RUR"}).convert_currency_average()
        3000
        >>> type(Salary({"salary_from": 1000,"salary_to": '5000',"salary_gross": 'False',"salary_currency": "RUR"}).salary_to)
        <class 'int'>
        """
        for key in salary:
            try:
                setattr(self, key, int(float(salary[key])))
            except ValueError:
                setattr(self, key, salary[key])
        if self.salary_from and self.salary_to:
            self.salary_average = int((self.salary_from + self.salary_to) / 2)

    def convert_currency_average(self):
        """ Конвертирует и возвращает среднюю зарплату в рублях

        :return: Среднюю зарплату в рублях
        :rtype: float
        """
        return self.salary_average * self._currency_to_rub[self.salary_currency]

if __name__ == "__main__":
    import doctest
    doctest.testmod()