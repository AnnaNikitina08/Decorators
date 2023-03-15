import os
import time
import datetime
import types


def logger(path):
    def _logger(old_function):
        old_function_name = old_function.__name__

        def wrapper(*args, **kwargs):
            print(f'Работает wrapper для {old_function}:')
            if os.path.exists(path):
                log_file = open(path, 'at', encoding='utf-8')
            else:
                print(f'\tНе найден файл "{path}"')
                log_file = open(path, 'wt', encoding='utf-8')
            print(f'\tОткрыт для записи файл "{path}"')

            start = time.time()
            res = old_function(*args, **kwargs)
            end = time.time()

            log_file.write(f'Дата и время вызова функции:" {old_function_name}": {datetime.datetime.now()}\n')
            log_file.write(f'\tВозвращаемое значение с аргументами "{args}, {kwargs}" - "{res}".\n')
            log_file.write(f'\tВремя выполнения: {end - start} секунд.\n')

            log_file.close()
            print(f'\tФайл "{path}" закрыт')
            return res

        return wrapper
    return _logger


list_of_lists = [
    ['a', 'b', 'c'],
    ['d', 'e', 'f'],
    [1, 2, None],
]


@logger(path='log3_1.log')
def flat_generator(list_of_list):
    for elem in list_of_list:
        for i in elem:
            yield i


for item in flat_generator(list_of_lists):
    print(item)


def test_3():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


if __name__ == '__main__':
    test_3()

