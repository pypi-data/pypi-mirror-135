import logging
import sys

if sys.argv[0].split("/")[-1] == 'client.py':
    LOGGER = logging.getLogger('client')
elif sys.argv[0].split("/")[-1] == 'server_start.py':
    LOGGER = logging.getLogger('server')


def log(func):
    def log_saver(*args, **kwargs):
        result = func(*args, **kwargs)
        LOGGER.debug(
            f'DECORATED '  # для удобства отладки
            f'Вызвана функция {func.__name__} с параметрами {args, kwargs} '
            f'из модуля {func.__module__}. ',
            stacklevel=2
        )
        return result
    return log_saver
