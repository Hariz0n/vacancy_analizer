import os

from DataSet import DataSet
from Report import Report
from Statistics import Statistic


class InputConnect:
    def __init__(self):
        self.file_name = input('Введите название файла: ').strip()
        self.work_name = input('Введите название профессии: ').strip()
        if self.is_valid():
            dataset: DataSet = DataSet(self.file_name)
            stats = Statistic(dataset, self.work_name)
            stats.print_statistic()
            report = Report(stats)
            report.generate_excel()
            report.generate_image()
            report.generate_pdf()

    def is_valid(self) -> bool:
        if os.stat(self.file_name).st_size == 0:
            print("Пустой файл")
            return False
        return True

    