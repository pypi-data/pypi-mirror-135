import binascii
import hmac
import json
import logging
import os
import select
import socket
import threading

from server.common.descriptors import ValidatePort, ValidateAddress
from server.common.utils import get_message, send_message
from server.common.variables import ACTION, PRESENCE, TIME, ACCOUNT_NAME, ERROR, \
    MESSAGE, MESSAGE_TEXT, SENDER_USER, EXIT, DESTINATION_USER, \
    ADD_CONTACT, RESPONSE_200, RESPONSE_400, REMOVE_CONTACT, GET_CONTACTS, \
    LIST_INFO, USER, GET_ALL_USERS, \
    MAX_CONNECTIONS, RESPONSE_511, DATA, RESPONSE, PUBLIC_KEY, RESPONSE_205, \
    PUBLIC_KEY_REQUEST

logger = logging.getLogger('server')

database_lock = threading.Lock()
message = None
new_connection = False
conflag_lock = threading.Lock()


class MessageProcessor(threading.Thread):
    listen_port = ValidatePort()
    listen_address = ValidateAddress()

    def __init__(self, database, listen_address, listen_port):
        self.server_socket = None
        self.listen_address = listen_address
        self.listen_port = listen_port
        self.database = database
        self.clients_list = []
        self.message_list = []
        self.users_list = {}
        self.listen_socket = None
        self.error_socket = None
        self.running = True

        super().__init__()

    def init_socket(self):
        logger.info(
            f'Запущен сервер, порт для подключений: {self.listen_port}, адрес'
            f' с которого принимаются подключения: {self.listen_address}.'
            f' Если адрес не указан, принимаются соединения с любых адресов.')

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.listen_address, self.listen_port))
        transport.settimeout(0.5)
        self.server_socket = transport
        self.server_socket.listen(MAX_CONNECTIONS)

    def run(self):
        global message
        global new_connection
        self.init_socket()
        while self.running:
            try:
                client, client_address = self.server_socket.accept()
            except OSError:
                pass
            else:
                logger.info(
                    f'Установлено соединение с клиентом {client_address}')
                client.settimeout(5)
                self.clients_list.append(client)

            read_data_list = []
            try:
                if self.clients_list:
                    read_data_list, self.listen_socket, self.error_socket = select.select(
                        self.clients_list,
                        self.clients_list,
                        [], 0)
            except OSError as error:
                logger.error(f'Ошибка работы с сокетами: {error.errno}')

            if read_data_list:
                for client_with_message in read_data_list:
                    try:
                        message = get_message(client_with_message)
                        self.process_client_message(message,
                                                    client_with_message)
                    except (OSError, json.JSONDecodeError, TypeError) as error:
                        logger.debug(
                            'Getting data from client exception.',
                            exc_info=error
                        )
                        self.remove_client(client_with_message)

    def remove_client(self, client):
        logger.info(f'Клиент {client.getpeername()} отключился от сервера.')
        for name in self.users_list:
            if self.users_list[name] == client:
                self.database.user_logout(name)
                del self.users_list[name]
                break
        self.clients_list.remove(client)
        client.close()

    def check_user_and_send_message(self, message):
        if message[DESTINATION_USER] in self.users_list and \
                self.users_list[
                    message[DESTINATION_USER]] in self.listen_socket:
            try:
                print('message - ', message)
                print(self.users_list)
                send_message(message,
                             self.users_list[message[DESTINATION_USER]])
                logger.info(
                    f'Отправлено сообщение пользователю'
                    f' {message[DESTINATION_USER]} от пользователя'
                    f' {message[SENDER_USER]}.'
                )
            except OSError:
                self.remove_client(message[DESTINATION_USER])
        elif message[DESTINATION_USER] in self.users_list and \
                self.users_list[
                    message[DESTINATION_USER]] not in self.listen_socket:
            logger.error(
                f'Связь с клиентом {message[DESTINATION_USER]} была потеряна.'
                f' Соединение закрыто, доставка невозможна.'
            )
            self.remove_client(self.users_list[message[DESTINATION_USER]])
        else:
            logger.error(
                f'Пользователь {message[DESTINATION_USER]} '
                f'не зарегистрирован на сервере.'
            )

    def process_client_message(self, message, client):
        """Обработчик сообщений от клиентов"""
        logger.debug(f'Разбор сообщения от клиента : {message}')
        # Сообщение о присутствии
        if ACTION in message and message[ACTION] == PRESENCE \
                and TIME in message and ACCOUNT_NAME in message:
            self.autorize_user(message, client)
        # Сообщение с текстом
        elif ACTION in message and message[ACTION] == MESSAGE and \
                TIME in message and MESSAGE_TEXT in message:
            if message[DESTINATION_USER] in self.users_list:
                self.check_user_and_send_message(message)
                self.database.increment_sent_accepted_message(
                    message[SENDER_USER], message[DESTINATION_USER])
                try:
                    send_message(RESPONSE_200, client)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Пользователь не зарегистрирован на сервере'
                try:
                    send_message(response, client)
                except OSError:
                    pass
            return
        # Сообщение добавление контакта
        elif ACTION in message and message[ACTION] == ADD_CONTACT and \
                USER in message and ACCOUNT_NAME in message:
            self.database.add_contact(message[ACCOUNT_NAME], message[USER])
            try:
                send_message(RESPONSE_200, client)
            except OSError:
                self.remove_client(client)
            return
        # Сообщение удаление контакта
        elif ACTION in message and message[ACTION] == REMOVE_CONTACT and \
                USER in message and ACCOUNT_NAME in message:
            self.database.remove_contact(message[ACCOUNT_NAME], message[USER])
            try:
                send_message(RESPONSE_200, client)
            except OSError:
                self.remove_client(client)
            return
        # Сообщение запрос списка контактов
        elif ACTION in message and message[ACTION] == GET_CONTACTS and\
                ACCOUNT_NAME in message:
            response = RESPONSE_200
            response[LIST_INFO] = self.database.get_contacts(
                message[ACCOUNT_NAME])
            try:
                send_message(response, client)
            except OSError:
                self.remove_client(client)
            return
        # Сообщение запрос списка контактов
        elif ACTION in message and message[ACTION] == GET_ALL_USERS:
            response = RESPONSE_200
            response[LIST_INFO] = [user[0] for user in
                                   self.database.users_list()]
            try:
                send_message(response, client)
            except OSError:
                self.remove_client(client)
            return
        # Сообщение запрос на выход
        elif ACTION in message and message[ACTION] == EXIT and\
                ACCOUNT_NAME in message:
            self.remove_client(client)
        elif ACTION in message and message[ACTION] == PUBLIC_KEY_REQUEST and\
                ACCOUNT_NAME in message:
            response = RESPONSE_511
            response[DATA] = self.database.get_public_key(
                message[ACCOUNT_NAME])
            if response[DATA]:
                try:
                    send_message(response, client)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESPONSE_400
                response[
                    ERROR] = 'Нет публичного ключа для данного пользователя'
                try:
                    send_message(response, client, )
                except OSError:
                    self.remove_client(client)
        else:
            send_message(RESPONSE_400, client)

    def autorize_user(self, message, client):
        logger.debug(f'Запущен процесс авторизации {message[ACCOUNT_NAME]}')
        if message[ACCOUNT_NAME] in self.users_list.keys():
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято'
            try:
                send_message(response, client)
            except OSError:
                pass
            else:
                self.clients_list.remove(client)
                client.close()

        elif not self.database.check_user(message[ACCOUNT_NAME]):
            response = RESPONSE_400
            response[ERROR] = 'Пользователь не зарегистрирован'
            try:
                send_message(response, client)
            except OSError:
                pass
            else:
                self.clients_list.remove(client)
                client.close()
        else:
            logger.debug(
                'Пользователь корректный, начинается проверка пароля')

        message_auth = RESPONSE_511
        random_str = binascii.hexlify(os.urandom(64))
        message_auth[DATA] = random_str.decode('ascii')
        hash_password = hmac.new(
            self.database.get_password_hash(message[ACCOUNT_NAME]),
            random_str,
            'MD5'
        )
        print(self.database.get_password_hash(message[ACCOUNT_NAME]))
        digest = hash_password.digest()
        logger.debug(f'сообщение авторизации = {message_auth}')
        try:
            send_message(message_auth, client)
            ans = get_message(client)
        except OSError as error:
            logger.debug('Ошибка аутентификации', exc_info=error)
            client.close()
            return
        client_digest = binascii.a2b_base64(ans[DATA])
        print(digest, client_digest)
        if RESPONSE in ans and ans[RESPONSE] == 511 and hmac.compare_digest(
                digest, client_digest):
            self.users_list[message[ACCOUNT_NAME]] = client
            client_ip, client_port = client.getpeername()
            try:
                send_message(RESPONSE_200, client)
            except OSError:
                self.remove_client(client)
            self.database.user_login(message[ACCOUNT_NAME], client_ip,
                                     client_port, message[PUBLIC_KEY])

        else:
            response = RESPONSE_400
            response[ERROR] = 'Неверный пароль.'
            try:
                send_message(response, client)
            except OSError:
                pass
            self.clients_list.remove(client)
            client.close()

    def service_update_lists(self):
        for client in self.users_list:
            try:
                send_message(self.users_list[client], RESPONSE_205)
            except OSError:
                self.remove_client(self.users_list[client])


if __name__ == '__main__':
    pass
