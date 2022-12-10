import os

import pandas as pd


def csv_splitter(file_name: str):
    """
    Разделяет переданный csv файл по годам
    :return: None
    """
    data = pd.read_csv(file_name, index_col=0, engine="pyarrow").dropna()
    name = file_name.replace('.csv', '')
    years = data['published_at'].dt.year.unique()
    os.makedirs(name, exist_ok=True)
    for year in [y for y in years if y is not None]:
        if not year:
            continue
        data[data['published_at'].dt.year == year].to_csv(f'{name}/{year}.csv')
