from pprint import pprint

import requests
import csv

from abc import abstractmethod, ABC
from bs4 import BeautifulSoup
from datetime import datetime, timezone


class DataClient(ABC):
    urls = 'https://www.kufar.by/l/mebel'
    _fieldnames = ('LINK', 'PRICE', 'DESCRIPTION')
    # _pattern = "%d-%m-%Y %H.%M"
    _pattern_date = "%d-%m-%Y"
    TABLE_NAME = "app_1_mebel"

    @abstractmethod
    def connect_to_db(self):
        pass

    @abstractmethod
    def create_table_db(self, connection):
        pass

    def close_connection_db(self, connection):
        if connection:
            connection.close()

    def get_data_from_url(self):
        self.data = []
        response = requests.get(self.urls).text
        soup = BeautifulSoup(response, 'html.parser')
        links = soup.find_all('a', class_='styles_wrapper__5FoK7')
        for link in links:
            data = link.text.split(' р.')
            try:
                price, description = data
                # следующий if т к при одном из запросов в цену попала строка с текстом.
                # Пример: "Онлайн покупка1382"
                price = ''.join(char for char in price if char.isdigit())
            except:
                price = 0
                description = data[0]
            # словарь выбран для записи в csv через модуль csv объект DictWriter
            self.data.append(
                {
                    'LINK': link['href'],
                    'PRICE': price,
                    'DESCRIPTION': description
                }
            )

    # def write_to_csv(self):
    #
    #     with open(f'{datetime.now().strftime(self._pattern_date)} kufar_mebel.csv', 'w', encoding='utf-8-sig',
    #               newline='') as f:
    #         writer = csv.DictWriter(f, fieldnames=self._fieldnames, delimiter=';')
    #         writer.writeheader()
    #         for item in self.data:
    #             writer.writerow(item)
    #
    #
    # def write_to_csv_pandas(self):
    #     df = pd.DataFrame(self.data)
    #     df.to_csv(f'{datetime.now().strftime(self._pattern_date)} kufar_mebel.csv', sep=';', encoding='utf-8-sig', index=False)
    #

    @staticmethod
    def get_csv_filename():
        import os
        import re

        pattern_filename = r".+\.csv"
        list_of_files = []
        for file in os.listdir(os.curdir):
            filter_for_files = re.search(pattern_filename, file)
            if filter_for_files:
                list_of_files.append(file)

        return list_of_files

    def read_from_csv(self):
        '''
        МОДУЛЬ CSV
        кодировка "utf-8-sig" мне на работе позволила не волноваться в
        какой программе открывать файл. Программы под линукс, или windows русский текст при
        такой кодировке распознавали =)
        :param file_name:
        :return: None
        '''
        file_name = self.get_csv_filename()
        if isinstance(file_name, list) and len(file_name) == 1:
            with open(*file_name, encoding='utf-8-sig') as from_file:
                reader = csv.DictReader(from_file, delimiter=';')
                for num, line in enumerate(reader, 1):
                    print(
                        f"{num}) {line.get('LINK', '[INFO] Значения в файле нет!')}\n\t\t{line.get('PRICE', '[INFO] Значения в файле нет!')}\n\t\t{line.get('DESCRIPTION', '[INFO] Значения в файле нет!')}")
            return
        print(f'Список доступных файлов: {file_name}')

    # def read_from_csv_with_pandas(self):
    #     '''
    #     МОДУЛЬ Pandas
    #     :param file_name:
    #     :return: None
    #     '''
    #
    #     from itertools import zip_longest
    #
    #     file_name = self.get_csv_filename()
    #     fieldnames = ['LINK', 'PRICE', 'DESCRIPTION']
    #     message_info = '[INFO] Значения в файле нет!'
    #     if isinstance(file_name, list) and len(file_name) == 1:
    #         df = pd.read_csv(*file_name, delimiter=';', encoding='utf-8-sig')
    #         for num, line in enumerate(df.values.tolist()):
    #             # print(str(line[2]))
    #             # break
    #             line = dict(zip_longest(fieldnames, line))
    #             link = line.get('LINK')
    #             price = line.get('PRICE')
    #             description = line.get('DESCRIPTION')
    #             print(
    #                 f"{num}) {link if str(link) != 'nan' else message_info}\n\t\t{price if str(price) != 'nan' else message_info}\n\t\t{description if str(description) != 'nan' else message_info}")
    #
    #         return
    #     print(f'Список доступных файлов: {file_name}')

    def insert_to_db(self, connection):
        if connection:
            cursor = connection.cursor()
            dt = datetime.now(timezone.utc).astimezone()
            for item in self.data:
                link, price, description = item.values()
                # не придумал пока что как исделать в одну строку VALUES (), (), ()
                cursor.execute(
                    f"INSERT INTO {self.TABLE_NAME} (link, price, description, parse_datetime) VALUES ('{link}', '{price}', '{description}', '{dt}')")
            connection.commit()
        else:
            print(connection, 'ERROR CONNECTION TO DB!')


    def erase_db(self, connection):
        if connection:
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM {self.TABLE_NAME}")
            connection.commit()

    def clear_self_data(self):
        self.data.clear()

    @abstractmethod
    def get_data_from_db(self):
        pass

    def run(self):
        self.get_data_from_url()

        # self.write_to_csv()
        # self.write_to_csv_pandas()

        connection_to_db = self.connect_to_db()
        self.create_table_db(connection_to_db)
        self.insert_to_db(connection_to_db)
        self.close_connection_db(connection_to_db)
        self.clear_self_data()
#
