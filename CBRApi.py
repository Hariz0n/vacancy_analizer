from datetime import datetime
import requests
import pandas as pd
from db import DB


class CBRApi:
    @staticmethod
    def getCurrenciesValues(earliest: datetime, latest: datetime, needed_curs: list[str] = None) -> pd.DataFrame:
        """Метод получения данных о курсах валют в заданный период времени

        :param earliest: дата начала сбора данных о курсе валют
        :type earliest: datetime
        :param latest: дата окончания сбора данных о курсе валют
        :type latest: datetime
        :param needed_curs: список  необходимый валют
        :type needed_curs: list[str]
        :return: ДадаФрейм данных о необходимых курсах валют на заданный период
        :rtype: pd.DataFrame
        """
        result = None
        for date in pd.date_range(start=earliest, end=latest + pd.offsets.MonthEnd(), freq='M', normalize=True, inclusive='both'):
            data = pd.read_xml(requests.get(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={date.strftime("%d/%m/%Y")}').text)
            data[date.strftime("%Y-%m")] = (data['Value'].str.replace(',', '.').astype(float) / data['Nominal']).round(5)
            table = data[['CharCode', date.strftime("%Y-%m")]].set_index('CharCode').T
            if result is None:
                result = pd.DataFrame(columns=table.columns)
            result = pd.concat([result, table])
        if not needed_curs:
            result.to_csv('curs.csv', index_label='date')
            return result

        DB().addData(result)
        result[needed_curs].to_csv('curs.csv', index_label='date')
        return result[needed_curs]


data = pd.read_csv('vacancies_dif_currencies.csv', engine='pyarrow')
data = data[data.groupby("salary_currency")['salary_currency'].transform('size') > 5000]\
    .sort_values(['published_at'])
earliest = data.iloc[0]['published_at']
latest = data.iloc[-1]['published_at']
CBRApi.getCurrenciesValues(earliest, latest, data['salary_currency'].value_counts().index.drop(labels=['', 'RUR']).tolist())