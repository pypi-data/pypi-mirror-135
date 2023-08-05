import argparse
import configparser
import os
import sys
import threading

from PyQt5.QtWidgets import QApplication

from server.common.variables import DEFAULT_PORT
from server.main.core import MessageProcessor
from server.main.database import ServerStorage
from server.gui.main_window import MainWindow

database_lock = threading.Lock()
new_connection = False
conflag_lock = threading.Lock()


def parse_arg(default_port, default_address):
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default=default_address, nargs='?')
    parser.add_argument('-p', default=default_port, type=int, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    return listen_address, listen_port


def config_load():
    config = configparser.ConfigParser()
    dir_path = os.getcwd()
    config.read(f'server.ini')
    # Если конфиг файл загружен правильно, запускаемся,
    # иначе конфиг по умолчанию.
    if 'SETTINGS' in config:
        return config
    else:
        config.add_section('SETTINGS')
        config.set('SETTINGS', 'Default_port', str(DEFAULT_PORT))
        config.set('SETTINGS', 'Listen_Address', '')
        config.set('SETTINGS', 'Database_path', dir_path)
        config.set('SETTINGS', 'Database_file', 'server_database.db3')
        return config


def main():
    config = config_load()
    listen_address, listen_port = parse_arg(
        config['SETTINGS']['Default_port'],
        config['SETTINGS']['Listen_Address']
    )
    database = ServerStorage(
        os.path.join(
            config['SETTINGS']['Database_path'],
            config['SETTINGS']['Database_file']
        )
    )

    server = MessageProcessor(database, listen_address, listen_port)
    server.daemon = True
    server.start()

    server_app = QApplication(sys.argv)
    main_window = MainWindow(database, server, config)

    server_app.exec_()
    server.running = False


if __name__ == '__main__':
    main()
