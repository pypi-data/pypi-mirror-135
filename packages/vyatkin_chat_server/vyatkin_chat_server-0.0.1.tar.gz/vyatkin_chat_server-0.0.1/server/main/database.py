import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, Integer,\
    String, DateTime, ForeignKey, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator


class ServerStorage:
    class AllUser:
        """Класс - отображение таблицы все пользователей"""
        def __init__(self, username, password_hash):
            self.name = username
            self.last_login = datetime.datetime.now()
            self.id = None
            self.password_hash = password_hash
            self.public_key = None

    class ActiveUser:
        """Класс- отображение таблицы всех активных пользователей"""
        def __init__(self, user_id, ip_address, port, at_login_time):
            self.id = None
            self.user = user_id
            self.ip_address = ip_address
            self.port = port
            self.at_login_time = at_login_time

    class LoginHistory:
        def __init__(self, username, date, ip, port):
            self.id = None
            self.name = username
            self.ip = ip
            self.port = port
            self.date = date

    class UserContacts:
        def __init__(self, user, contact):
            self.id = None
            self.user = user
            self.contact = contact

    class UserHistory:
        def __init__(self, user):
            self.id = None
            self.user = user
            self.sent = 0
            self.accepted = 0

    def __init__(self, path):
        server_database = f'sqlite:///{path}'
        self.database_engine = create_engine(
            server_database,
            echo=False,
            pool_recycle=7200,
            connect_args={
                'check_same_thread': False
            }
        )
        self.metadata = MetaData()

        users_table = Table('Users', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String, unique=True),
                            Column('last_login', DateTime),
                            Column('password_hash', String),
                            Column('public_key', Text),
                            )
        active_users_table = Table('Active_users', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('user', ForeignKey('Users.id'),
                                          unique=True),
                                   Column('ip_address', String),
                                   Column('port', Integer),
                                   Column('at_login_time', DateTime),
                                   )
        login_history_table = Table('Login_history', self.metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('user', ForeignKey('Users.id'),
                                           unique=True),
                                    Column('ip_address', String),
                                    Column('port', Integer),
                                    Column('date', DateTime),
                                    )
        contacts_table = Table('Contacts', self.metadata,
                               Column('id', Integer, primary_key=True),
                               Column('user', ForeignKey('Users.id')),
                               Column('contact', ForeignKey('Users.id')),
                               )
        user_history_table = Table('User_history', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('user', ForeignKey('Users.id')),
                                   Column('sent', Integer),
                                   Column('accepted', Integer),
                                   )

        self.metadata.create_all(self.database_engine)
        mapper(self.AllUser, users_table)
        mapper(self.ActiveUser, active_users_table)
        mapper(self.LoginHistory, login_history_table)
        mapper(self.UserContacts, contacts_table)
        mapper(self.UserHistory, user_history_table)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        self.session.query(self.ActiveUser).delete()
        self.session.commit()

    def user_login(self, username, ip_address, port, key):
        result = self.session.query(self.AllUser).filter_by(name=username)
        if result.count():
            user = result.first()
            user.last_login = datetime.datetime.now()
            if user.public_key != key:
                user.public_key = key
        else:
            raise ValueError(f'Пользователь не зарегистрирован')

        new_active_user = self.ActiveUser(
            user.id,
            ip_address,
            port,
            datetime.datetime.now()
        )
        self.session.add(new_active_user)

        self.LoginHistory(
            user.id,
            ip_address,
            port,
            datetime.datetime.now()
        )
        self.session.add(new_active_user)
        self.session.commit()

    def add_user(self, username, password_hash):
        user = self.AllUser(username, password_hash)
        self.session.add(user)
        self.session.commit()
        user_in_history = self.UserHistory(user.id)
        self.session.add(user_in_history)
        self.session.commit()

    def remove_user(self, username):
        user = self.session.query(self.AllUser).filter_by(
            name=username).first()
        self.session.query(self.LoginHistory).filter_by(user=user.id).delete()
        self.session.query(self.ActiveUser).filter_by(user=user.id).delete()
        self.session.query(self.UserContacts).filter_by(user=user.id).delete()
        self.session.query(self.UserHistory).filter_by(user=user.id).delete()
        self.session.query(self.AllUser).filter_by(id=user.id).delete()

        self.session.commit()

    def get_password_hash(self, username):
        user = self.session.query(self.AllUser).filter_by(
            name=username).first()
        return user.password_hash

    def get_public_key(self, username):
        user = self.session.query(self.AllUser).filter_by(
            name=username).first()
        return user.public_key

    def check_user(self, username):
        user = self.session.query(self.AllUser).filter_by(
            name=username).count()
        if user:
            return True
        else:
            return False

    def user_logout(self, username):
        user = self.session.query(self.AllUser).filter_by(
            name=username).first()
        self.session.query(self.ActiveUser).filter_by(user=user.id).delete()
        self.session.commit()

    def users_list(self):
        query = self.session.query(
            self.AllUser.name,
            self.AllUser.last_login
        ).all()
        return query

    def active_users_list(self):
        query = self.session.query(
            self.AllUser.name,
            self.ActiveUser.ip_address,
            self.ActiveUser.port,
            self.ActiveUser.at_login_time,
        ).join(self.AllUser).all()
        return query

    def login_history_list(self, username=None):
        query = self.session.query(
            self.AllUser.name,
            self.LoginHistory.ip_address,
            self.LoginHistory.port,
            self.LoginHistory.date,
        ).join(self.AllUser)
        if username:
            query = query.filter(self.AllUser.name == username)
        return query.all()

    def increment_sent_accepted_message(self, sender, recipient):
        sender_id = self.session.query(self.AllUser).filter_by(
            name=sender).first().id
        recipient_id = self.session.query(self.AllUser).filter_by(
            name=recipient).first().id
        sender_history = self.session.query(self.UserHistory).filter_by(
            user=sender_id).first()
        sender_history.sent += 1
        recipient_history = self.session.query(self.UserHistory).filter_by(
            user=recipient_id).first()
        recipient_history.accepted += 1
        self.session.commit()

    def add_contact(self, user, contact):
        user = self.session.query(self.AllUser).filter_by(name=user).first()
        contact = self.session.query(self.AllUser).filter_by(
            name=contact).first()
        if not contact or self.session.query(self.UserContacts).filter_by(
                user=user.id, contact=contact.id).count():
            return
        row = self.UserContacts(user.id, contact.id)
        self.session.add(row)
        self.session.commit()

    def remove_contact(self, user, contact):
        user = self.session.query(self.AllUser).filter_by(name=user).first()
        contact = self.session.query(self.AllUser).filter_by(
            name=contact).first()
        if not contact:
            return
        self.session.query(self.UserContacts).filter_by(
            user=user.id, contact=contact.id).delete()
        self.session.commit()

    def get_contacts(self, username):
        user = self.session.query(self.AllUser).filter_by(name=username).one()
        query = self.session.query(
            self.UserContacts.user,
            self.AllUser.name
        ).filter_by(user=user.id).join(
            self.AllUser,
            self.UserContacts.contact == self.AllUser.id
        )
        return [contact[1] for contact in query.all()]

    def message_history(self, username=None):
        query = self.session.query(
            self.AllUser.name,
            self.UserHistory.sent,
            self.UserHistory.accepted
        ).join(self.AllUser)
        if username:
            query = query.filter_by(name=username)
        return query.all()
