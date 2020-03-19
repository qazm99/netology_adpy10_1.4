import json
from hashlib import md5
from datetime import datetime
import os


def log_function(filename_log):
    def decorator(in_function):
        def modify_function(*args,**kwargs):
            out_function = in_function(*args, **kwargs)
            path_file = filename_log[:filename_log.rfind('/')]
            if not os.path.exists(path_file):
                os.makedirs(path_file)
            with open(filename_log, 'a', encoding='utf-8') as file_log:
                file_log.write(f'{datetime.now()}, name_function-{in_function.__name__}, '
                               f'parametrs-{args},{kwargs}, result-{out_function} \n')
            return out_function
        return modify_function
    return decorator

class Country_json:
    def __init__(self, file):
        self.file = file
        self.country_list = []
        with open(self.file, encoding='utf-8') as json_file:
            self.json_file = json_file
            for country in json.load(self.json_file):
                self.country_list.append(country['name']['common'])

    def __iter__(self):
        self.iter_num = 0
        return self

    def __next__(self):
        self.iter_num += 1
        if self.iter_num > len(self.country_list):
            raise StopIteration
        return {self.country_list[self.iter_num - 1]: 'https://en.wikipedia.org/wiki/' + self.country_list[
            self.iter_num - 1].replace(' ', '_')}


@log_function('logs/dict_accumulator.txt')
def dict_accumulator(iter_class):
    dict_all = {}
    for item in iter_class:
        if isinstance(item, dict):
            dict_all.update(item)
        else:
            print('Необходим тип данных dict')
    return dict_all

@log_function('logs/save_dict_json.txt')
def save_dict_json(dict_in, filename):
    if isinstance(dict_in, dict):
        with open(filename, "w") as file:
            json.dump(dict_in, file)
    else:
        print('Могу сохранить в json только dict')

@log_function('logs/line_md5.txt')
def line_md5(filename):
    with open(filename, encoding='utf-8') as file_data:
        for line in file_data:
            yield line


if __name__ == '__main__':
    print('Давайте попробуем в файле найти страны и сформировать ссылки на их страницы в википедии \n' +
          'и сохраним все в файл:')
    try:
        url_file = 'country-url.json'
        save_dict_json(dict_accumulator(Country_json('countries.json')), url_file)
        print(f'Ссылки на википедию успешно сформированы в файл {url_file}')
    except FileNotFoundError:
        print('Файл для чтения данных со странами не найден')
    print('А сейчас мы попробуем построчно получить хэш строк этого файла')
    input('Продолжить?(Enter)')
    try:
        for num_line, line in enumerate(line_md5('countries.json')):
            print(f'Строка {num_line}: {md5(line.encode("utf-8")).hexdigest()}')
    except FileNotFoundError:
        print('Файл для хэша строк не найден')


