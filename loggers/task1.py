import os
import time
import datetime


def logger(old_function):
    path = 'main.log'
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


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'

    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()
