import datetime
import os.path

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, \
    String, Text, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator


class ClientDatabase:
    class KnownUsers:
        """Класс - отображения всех пользователей"""
        def __init__(self, username):
            self.id = None
            self.username = username

    class MessageHistory:
        """Класс - отображение статистики сообщений"""
        def __init__(self, contact, direction, message):
            self.id = None
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = datetime.datetime.now()

    class Contacts:
        """Класс - отображение контактов"""
        def __init__(self, contact):
            self.id = None
            self.name = contact

    def __init__(self, name):
        self.database_engine = create_engine(
            f'sqlite:///{os.getcwd()}/files/{name}/client_database.db3',
            echo=False,
            pool_recycle=7200,
            connect_args={'check_same_thread': False}
        )
        self.metadata = MetaData()

        known_users_table = Table('known_users', self.metadata,
                                  Column('id', Integer, primary_key=True),
                                  Column('username', String),
                                  )
        message_history = Table('message_history', self.metadata,
                                Column('id', Integer, primary_key=True),
                                Column('contact', String),
                                Column('direction', String),
                                Column('message', Text),
                                Column('date', DateTime),
                                )
        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String),
                         )
        self.metadata.create_all(self.database_engine)
        mapper(self.KnownUsers, known_users_table)
        mapper(self.MessageHistory, message_history)
        mapper(self.Contacts, contacts)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        self.session.query(self.Contacts).delete()
        self.session.commit()

    def add_contact(self, contact):
        """Добавление контакта в базу"""
        if not self.session.query(self.Contacts).filter_by(
                name=contact).count():
            row = self.Contacts(contact)
            self.session.add(row)
            self.session.commit()

    def delete_contact(self, contact):
        """Удаление контакта из базы"""
        self.session.query(self.Contacts).filter_by(name=contact).delete()
        self.session.commit()

    def add_users(self, users_list: list):
        """Заполняет таблицу пользователей"""
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            row = self.KnownUsers(user)
            self.session.add(row)
        self.session.commit()

    def save_message(self, contact, direction, message):
        """Сохраняет сообщения в базу"""
        row = self.MessageHistory(contact, direction, message)
        self.session.add(row)
        self.session.commit()

    def get_contacts_list(self):
        """Возвращает список контактов"""
        return [contact.name for contact in
                self.session.query(self.Contacts).all()]

    def get_user_list(self):
        """Возвращает список пользователей"""
        query = self.session.query(self.KnownUsers)
        return [user.username for user in query.all()]

    def check_contact(self, contact):
        """Проверят наличие контакта"""
        if self.session.query(self.Contacts).filter_by(name=contact).count():
            return True
        else:
            return False

    def get_history(self, contact=None, direction=None):
        """Возвращает список с историей сообщения"""
        query = self.session.query(self.MessageHistory)
        if contact:
            query = query.filter_by(contact=contact)
        if direction == 'in':
            query = query.filter_by(direction='in')
        if direction == 'out':
            query = query.filter_by(direction='out')
        return [(row.contact, row.direction, row.message, row.date) for row in
                query.all()]
