from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow:

    def __init__(self):
        self.centralwidget = None

    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(605, 364)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.contacts_list = QtWidgets.QListView(self.centralwidget)
        self.contacts_list.setGeometry(QtCore.QRect(10, 30, 191, 241))
        self.contacts_list.setObjectName("ContactlistView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 101, 17))
        self.label.setObjectName("label")
        self.list_messages = QtWidgets.QListView(self.centralwidget)
        self.list_messages.setGeometry(QtCore.QRect(230, 30, 361, 151))
        self.list_messages.setObjectName("MessageHistorylistView")
        self.text_message = QtWidgets.QTextEdit(self.centralwidget)
        self.text_message.setGeometry(QtCore.QRect(230, 210, 361, 61))
        self.text_message.setObjectName("MessageTextEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(240, 190, 141, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(240, 10, 121, 17))
        self.label_3.setObjectName("label_3")
        self.btn_add_contact = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add_contact.setGeometry(QtCore.QRect(10, 280, 89, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_add_contact.setFont(font)
        self.btn_add_contact.setObjectName("btn_add_contact")
        self.btn_delete_contact = QtWidgets.QPushButton(self.centralwidget)
        self.btn_delete_contact.setGeometry(QtCore.QRect(110, 280, 89, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_delete_contact.setFont(font)
        self.btn_delete_contact.setObjectName("btn_delete_contact")
        self.btn_send_message = QtWidgets.QPushButton(self.centralwidget)
        self.btn_send_message.setGeometry(QtCore.QRect(500, 280, 89, 25))
        self.btn_send_message.setObjectName("btn_send_message")
        self.btn_clean_message = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clean_message.setGeometry(QtCore.QRect(400, 280, 89, 25))
        self.btn_clean_message.setObjectName("btn_clean_message")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 605, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Contact list:"))
        self.label_2.setText(_translate("MainWindow", "Message:"))
        self.label_3.setText(_translate("MainWindow", "Message history:"))
        self.btn_add_contact.setText(_translate("MainWindow", "Add contact"))
        self.btn_delete_contact.setText(
            _translate("MainWindow", "Delete contact"))
        self.btn_send_message.setText(_translate("MainWindow", "Send message"))
        self.btn_clean_message.setText(
            _translate("MainWindow", "Clean message"))
        self.menuFile.setTitle(_translate("MainClientWindow", "File"))
        self.actionExit.setText(_translate("MainClientWindow", "Exit"))

    # Заполняем список возможных контактов разницей между всеми пользователями и
    def possible_contacts_update(self):
        self.selector.clear()
        # множества всех контактов и контактов клиента
        contacts_list = set(self.database.get_contacts_list())
        users_list = set(self.database.get_user_list())
        # Удалим сами себя из списка пользователей, чтобы нельзя было добавить самого себя
        users_list.remove(self.transport.username)
        # Добавляем список возможных контактов
        self.selector.addItems(users_list - contacts_list)

    # Обновлялка возможных контактов. Обновляет таблицу известных пользователей,
    # затем содержимое предполагаемых контактов
    def update_possible_contacts(self):
        try:
            self.transport.user_list_update()
        except OSError:
            pass
        else:
            # logger.debug('Обновление списка пользователей с сервера выполнено')
            self.possible_contacts_update()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    Dialog.show()
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
