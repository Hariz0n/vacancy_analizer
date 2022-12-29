import sqlite3

import pandas as pd
from pandas import DataFrame


class DB:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DB, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.con = sqlite3.connect('db.sqlite')
        self.cur = self.con.cursor()

    def addData(self, df: DataFrame):
        df.to_sql('currencies', self.con, if_exists='append', index_label='date')
