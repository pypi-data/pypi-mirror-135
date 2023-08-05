import binascii
import hashlib
import hmac
import json
import logging
import socket
import threading
import time

from PyQt5.QtCore import QObject, pyqtSignal

from common.errors import ServerError
from common.utils import get_message, send_message
from common.variables import RESPONSE, PRESENCE, ACCOUNT_NAME, ACTION, TIME, \
    GET_CONTACTS, LIST_INFO, GET_ALL_USERS, \
    REMOVE_CONTACT, USER, ADD_CONTACT, EXIT, MESSAGE, SENDER_USER, \
    DESTINATION_USER, MESSAGE_TEXT, PUBLIC_KEY, ERROR, \
    DATA, RESPONSE_511, PUBLIC_KEY_REQUEST

from project_logs.config import config_client_log


sock_lock = threading.Lock()
logger = logging.getLogger('client')


class ClientTransport(threading.Thread, QObject):
    new_message = pyqtSignal(dict)
    message_205 = pyqtSignal()
    connection_lost = pyqtSignal()

    def __init__(self, address, port, username, database, password, keys):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        self.transport = None
        self.address = address
        self.port = port
        self.username = username
        self.database = database
        self.password = password
        self.keys = keys
        self.connection_init()

        try:
            self.users_list_update()
            self.contacts_list_update()
        except OSError as err:
            if err.errno:
                logger.critical('Потеряно соединение с сервером.')
                raise ServerError('Потеряно соединение с сервером!')
            logger.error(
                'Timeout соединения при обновлении списков пользователей.')
        except json.JSONDecodeError:
            logger.critical('Потеряно соединение с сервером.')
            raise ServerError('Потеряно соединение с сервером!')
        self.running = True

    def connection_init(self):
        """Инициализирует подключение сокета"""
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.transport.settimeout(5)
        connected = False
        for _ in range(1):
            logger.info('Попытка подключения ... ')
            try:
                self.transport.connect((self.address, self.port))
                print(self.address, self.port)
            except (OSError, ConnectionRefusedError) as err:
                logger.error('connection error', err)
            else:
                logger.debug('connection success')
                connected = True
                break
            time.sleep(1)
        if not connected:
            logger.critical('Не удалось установить соединение с сервером')
            raise ServerError('Не удалось установить соединение с сервером')

        password_bytes = self.password.encode('utf-8')
        salt = self.username.lower().encode('utf-8')
        password_hash = hashlib.pbkdf2_hmac('sha512', password_bytes, salt,
                                            10000)
        password_hash_str = binascii.hexlify(password_hash)
        logger.debug(f'Passwd hash ready: {password_hash_str}')
        public_key = self.keys.publickey().export_key().decode('ascii')
        with sock_lock:
            try:
                send_message(self.create_presense_message(public_key),
                             self.transport)
                ans = get_message(self.transport)
                logger.debug(f'получен ответ {ans}')
                if RESPONSE in ans:

                    if ans[RESPONSE] == 511:
                        # Если всё нормально, то продолжаем процедуру
                        # авторизации.
                        ans_data = ans[DATA]
                        hash_password = hmac.new(
                            password_hash_str,
                            ans_data.encode('utf-8'),
                            'MD5'
                        )
                        digest = hash_password.digest()
                        my_ans = RESPONSE_511
                        my_ans[DATA] = binascii.b2a_base64(digest).decode(
                            'ascii')
                        send_message(my_ans, self.transport)
                        self.parse_input_message(get_message(self.transport))

                    elif ans[RESPONSE] == 400:
                        raise ServerError(ans[ERROR])

            except (OSError, json.JSONDecodeError) as err:
                logger.debug(f'Сбой соединения в процессе авторизации.',
                             exc_info=err)
                raise ServerError('Сбой соединения в процессе авторизации.')

    def create_presense_message(self, public_key):
        """Создает сообщение присутствия"""
        message = {
            ACTION: PRESENCE,
            TIME: time.time(),
            ACCOUNT_NAME: self.username,
            PUBLIC_KEY: public_key
        }
        logger.debug(f'Сформировано сообщение {message}')
        return message

    def key_request(self, user):
        """Отправляет запрос публичного ключа"""
        logger.debug(f'Запрос публичного ключа для {user}')
        req = {
            ACTION: PUBLIC_KEY_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: user
        }
        with sock_lock:
            send_message(req, self.transport)
            ans = get_message(self.transport)
        if RESPONSE in ans and ans[RESPONSE] == 511:
            return ans[DATA]
        else:
            logger.error(f'Не удалось получить ключ собеседника{user}.')

    def contacts_list_update(self):
        """Отправляет запрос на получение списка контактов"""
        message = {
            ACTION: GET_CONTACTS,
            ACCOUNT_NAME: self.username
        }
        logger.debug(f'Сформирован запрос {message}')
        with sock_lock:
            send_message(message, self.transport)
            ans = get_message(self.transport)
        logger.debug(f'Получен ответ {ans}')
        if ans[RESPONSE] == 200:
            for contact in ans[LIST_INFO]:
                self.database.add_contact(contact)
        else:
            logger.error(f'Не удалось обновить список контактов')

    def users_list_update(self):
        """Отправляет запрос на получение списка всех пользователей"""
        message = {
            ACTION: GET_ALL_USERS,
            USER: self.username
        }
        logger.debug(f'Сформирован запрос {message}')
        with sock_lock:
            send_message(message, self.transport)
            ans = get_message(self.transport)
        logger.debug(f'Получен ответ {ans}')
        if ans[RESPONSE] == 200:
            self.database.add_users(ans[LIST_INFO])
        else:
            logger.error(f'Не удалось обновить список контактов')

    def send_add_contact_message(self, contact):
        """Отправляет запрос на добавление контакта"""
        message = {
            ACTION: ADD_CONTACT,
            USER: contact,
            ACCOUNT_NAME: self.username
        }
        logger.debug(f'Сформирован запрос {message}')
        with sock_lock:
            send_message(message, self.transport)
            ans = get_message(self.transport)
        logger.debug(f'Получен ответ {ans}')
        if ans[RESPONSE] == 200:
            self.database.add_contact(contact)
            logger.debug(
                f'Добавлен контакт {contact} пользователю {self.username}')

    def send_remove_contact_message(self, contact):
        """Отправляет запрос на удаление контакта"""
        message = {
            ACTION: REMOVE_CONTACT,
            USER: contact,
            ACCOUNT_NAME: self.username
        }
        logger.debug(f'Сформирован запрос {message}')
        with sock_lock:
            send_message(message, self.transport)
            ans = get_message(self.transport)
        logger.debug(f'Получен ответ {ans}')
        if ans[RESPONSE] == 200:
            self.database.add_contact(contact)
            logger.debug(
                f'Удален контакт {contact} пользователю {self.username}')

    def send_exit_message(self):
        """Отправляет запрос на выход"""
        message = {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.username
        }
        logger.debug(f'Сформирован запрос {message}')
        with sock_lock:
            send_message(message, self.transport)
            ans = get_message(self.transport)
        logger.debug(f'Получен ответ {ans}')
        if ans[RESPONSE] == 200:
            self.running = False
            logger.debug('Транспорт завершает работу.')
            time.sleep(0.5)

    def send_client_message(self, contact, text):
        """Отправляет запрос с сообщением"""
        message = {
            ACTION: MESSAGE,
            SENDER_USER: self.username,
            DESTINATION_USER: contact,
            TIME: time.time(),
            MESSAGE_TEXT: text,
            ACCOUNT_NAME: self.username,
        }
        logger.debug(f'Сформирован запрос {message}')
        with sock_lock:
            send_message(message, self.transport)
            ans = get_message(self.transport)
        logger.debug(f'Получен ответ {ans}')
        # if ans[RESPONSE] == 200:
        #     self.databases.save_message(contact, direction, text)

    def parse_input_message(self, message):
        """Осуществляет разбор полученного сообщения от сервера"""
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return
            elif message[RESPONSE] == 400:
                raise ServerError(f'{message[ERROR]}')
            elif message[RESPONSE] == 205:
                self.user_list_update()
                self.contacts_list_update()
                self.message_205.emit()
            else:
                logger.error(
                    f'Принят неизвестный код подтверждения'
                    f' {message[RESPONSE]}'
                )
        if ACTION in message and message[ACTION] == MESSAGE and\
                SENDER_USER in message and DESTINATION_USER in message \
                and MESSAGE_TEXT in message and\
                message[DESTINATION_USER] == self.username:
            # self.database.save_message(message[SENDER_USER], 'in',
            #                                message[MESSAGE_TEXT])
            self.new_message.emit(message)
            logger.info(
                f'Получено сообщение от пользователя '
                f'{message[SENDER_USER]}:\n{message[MESSAGE_TEXT]}'
            )
        else:
            logger.error(
                f'Получено некорректное сообщение с сервера: {message}')

    def run(self):
        while self.running:
            time.sleep(1)
            with sock_lock:
                try:
                    self.transport.settimeout(0.5)
                    input_message = get_message(self.transport)
                    logger.debug(f'получено сообщение {input_message}')

                except (
                    ConnectionError,
                    ConnectionAbortedError,
                    ConnectionResetError,
                    json.JSONDecodeError,
                    TypeError
                ):
                    logger.debug('Потеряно соединение с сервером.')
                    self.running = False
                    self.connection_lost.emit()

                except OSError as err:
                    if err.errno:
                        logger.critical('Потеряно соединение с сервером.')
                        self.running = False
                        self.connection_lost.emit()
                # Проблемы с соединением
                else:
                    self.parse_input_message(input_message)
                finally:
                    self.transport.settimeout(5)
