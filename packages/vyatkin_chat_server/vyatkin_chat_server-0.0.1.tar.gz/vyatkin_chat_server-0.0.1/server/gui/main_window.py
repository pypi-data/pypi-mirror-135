from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QLabel, \
    QTableView

from server.gui.add_user import RegisterUser
from server.gui.config_window import ConfigWindow
from server.gui.remove_user import DelUserDialog
from server.gui.stat_window import StatWindow


class MainWindow(QMainWindow):
    def __init__(self, database, server, config):
        super(MainWindow, self).__init__()
        self.database = database
        self.server_thread = server
        self.config = config
        exitAction = QAction('Выход', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)
        self.refresh_button = QAction('Обновить список', self)
        self.config_btn = QAction('Настройки сервера', self)
        self.register_btn = QAction('Регистрация пользователя', self)
        self.remove_btn = QAction('Удаление пользователя', self)
        self.show_history_button = QAction('История клиентов', self)
        self.statusBar()
        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(self.refresh_button)
        self.toolbar.addAction(self.show_history_button)
        self.toolbar.addAction(self.config_btn)
        self.toolbar.addAction(self.register_btn)
        self.toolbar.addAction(self.remove_btn)
        self.setFixedSize(800, 600)
        self.setWindowTitle('alpha')

        self.label = QLabel('Список клиентов:', self)
        self.label.setFixedSize(240, 15)
        self.label.move(15, 35)
        self.label = QLabel('Список подключённых клиентов:', self)
        self.label.setFixedSize(240, 15)
        self.label.move(305, 35)
        self.all_clients_table = QTableView(self)
        self.all_clients_table.move(10, 55)
        self.all_clients_table.setFixedSize(150, 400)
        self.active_clients_table = QTableView(self)
        self.active_clients_table.move(300, 55)
        self.active_clients_table.setFixedSize(400, 400)

        timer = QTimer()
        timer.timeout.connect(self.gui_create_model_active_users)
        timer.timeout.connect(self.gui_create_model_all_users)
        timer.start(1000)

        # Связываем кнопки с процедурами
        self.refresh_button.triggered.connect(
            self.gui_create_model_active_users)
        self.show_history_button.triggered.connect(self.show_statistics)
        self.config_btn.triggered.connect(self.server_config)
        self.register_btn.triggered.connect(self.reg_user)
        self.remove_btn.triggered.connect(self.rem_user)
        self.show()

    def gui_create_model_active_users(self):
        """Создание модели активных пользователей"""
        list_users = self.database.active_users_list()
        lst = QStandardItemModel()
        lst.setHorizontalHeaderLabels(
            ['Имя Клиента', 'IP Адрес', 'Порт', 'Время подключения'])
        for row in list_users:
            user, ip, port, time = row
            user = QStandardItem(user)
            user.setEditable(False)
            ip = QStandardItem(ip)
            ip.setEditable(False)
            port = QStandardItem(str(port))
            port.setEditable(False)
            time = QStandardItem(str(time.replace(microsecond=0)))
            time.setEditable(False)
            lst.appendRow([user, ip, port, time])
        self.active_clients_table.setModel(lst)
        self.active_clients_table.resizeColumnsToContents()
        self.active_clients_table.resizeRowsToContents()

    def gui_create_model_all_users(self):
        """Создание модели всех пользователей"""
        list_users = self.database.users_list()
        lst = QStandardItemModel()
        lst.setHorizontalHeaderLabels(['Имя Клиента'])
        for row in list_users:
            user = row[0]
            user = QStandardItem(user)
            user.setEditable(False)
            lst.appendRow([user])
        self.all_clients_table.setModel(lst)
        self.all_clients_table.resizeColumnsToContents()
        self.all_clients_table.resizeRowsToContents()

    def show_statistics(self):
        """Метод создающий окно со статистикой клиентов."""
        global stat_window
        stat_window = StatWindow(self.database)
        stat_window.show()

    def server_config(self):
        """Метод создающий окно с настройками сервера."""
        global config_window
        # Создаём окно и заносим в него текущие параметры
        config_window = ConfigWindow(self.config)

    def reg_user(self):
        """Метод создающий окно регистрации пользователя."""
        global reg_window
        reg_window = RegisterUser(self.database, self.server_thread)
        reg_window.show()

    def rem_user(self):
        """Метод создающий окно удаления пользователя."""
        global rem_window
        rem_window = DelUserDialog(self.database, self.server_thread)
        rem_window.show()
