import logging

DEFAULT_PORT = 7880
DEFAULT_IP_ADDRESS = '127.0.0.1'
MAX_CONNECTIONS = 5
MAX_PACKAGE_LENGTH = 10240
ENCODING = 'utf-8'

ACTION = 'action'
TIME = 'time'
USER = 'user'
SENDER_USER = 'from'
DESTINATION_USER = 'to'
ACCOUNT_NAME = 'account_name'
EXIT = 'exit'

PRESENCE = 'presence'
MESSAGE = 'message'
ADD_CONTACT = 'add_contact'
USER_TO_ADDED = 'user_to_added'
REMOVE_CONTACT = 'remove_contact'
GET_CONTACTS = 'get_contacts'
GET_ALL_USERS = 'get_users_list'
LIST_INFO = 'contact_list'
MESSAGE_TEXT = 'message_text'
RESPONSE = 'response'
ERROR = 'error'
DATA = 'data'
PUBLIC_KEY = 'public_key'
PUBLIC_KEY_REQUEST = 'public_key_request'

RESPONSE_200 = {
    RESPONSE: 200
}
RESPONSE_205 = {
    RESPONSE: 205
}
RESPONSE_400 = {
    RESPONSE: 400
}
RESPONSE_511 = {
    RESPONSE: 511
}

LOGGING_LEVEL = logging.DEBUG

SERVER_DATABASE = f'sqlite:///server_database.db'
