class Salary:
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
        for key in salary:
            try:
                setattr(self, key, int(float(salary[key])))
            except ValueError:
                setattr(self, key, salary[key])
        if self.salary_from and self.salary_to:
            self.salary_average = int((self.salary_from + self.salary_to) / 2)

    def convert_currency_average(self):
        return self.salary_average * self._currency_to_rub[self.salary_currency]