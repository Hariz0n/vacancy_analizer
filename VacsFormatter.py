import os

import numpy as np
import pandas as pd
import multiprocessing as mp

import csv_splitter


class VacsFormatter:
    currencies = pd.read_csv('curs.csv', engine='pyarrow', index_col=0)
    @staticmethod
    def format(filename: str):
        data = pd.read_csv(f'vacancies_dif_currencies/{filename}', engine='pyarrow')
        data['salary'] = data.apply(VacsFormatter.getSalaryColumn, axis=1)
        data = data.drop(['salary_from', 'salary_to', 'salary_currency'], axis='columns')\
            .reindex(columns=['name', 'salary', 'area_name', 'published_at'])

        # print(data)
        return data

    @staticmethod
    def getDataframes():
        print(os.listdir('vacancies_dif_currencies'))
        with mp.Pool() as pl:
            stats = pl.map(VacsFormatter.format, os.listdir('vacancies_dif_currencies'))

        res = pd.concat(stats)
        res.head(100).to_csv('first-one-hundred.csv', index=False)
        res.to_csv('formatted.csv', index=False)


    @staticmethod
    def getSalaryColumn(row):
        if not pd.isnull(row['salary_from']) and not pd.isnull(row['salary_to']):
            salary = int((row['salary_from'] / row['salary_to']) / 2)
        elif not pd.isnull(row['salary_from']):
            salary = row['salary_from']
        elif not pd.isnull(row['salary_to']):
            salary = row['salary_to']
        else:
            salary = None
        if salary is None or row['salary_currency'] not in VacsFormatter.currencies.columns or \
                pd.isnull(VacsFormatter.currencies.loc[row['published_at'].strftime('%Y-%m')][row['salary_currency']]):
            return None
        else:
            return int(salary * VacsFormatter.currencies.loc[row['published_at'].strftime('%Y-%m')][row['salary_currency']])


# csv_splitter.csv_splitter('vacancies_dif_currencies.csv')


