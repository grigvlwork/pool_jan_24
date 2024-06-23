import sys
import traceback
import pyperclip
import qdarkstyle
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from datetime import datetime

BEGIN = datetime(2024, 5, 1)


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.hint1_le.textChanged.connect(self.create_my_answer)
        self.hint2_le.textChanged.connect(self.create_my_answer)
        self.hint3_le.textChanged.connect(self.create_my_answer)
        self.copy_answer_btn.clicked.connect(self.copy_my_answer)
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('hints.db')
        self.db.open()
        self.sql_env_rb.clicked.connect(self.choose_sql_model)
        self.python_env_rb.clicked.connect(self.choose_python_model)
        self.js_env_rb.clicked.connect(self.choose_js_model)
        self.html_env_rb.clicked.connect(self.choose_html_model)
        self.load_query = QSqlQuery(self.db)
        self.add_query = QSqlQuery(self.db)
        self.find_query = QSqlQuery(self.db)
        self.update_query = QSqlQuery(self.db)
        self.model = QSqlQueryModel()
        self.current_hint = None
        self.hints_tv.setModel(self.model)
        self.use_hint1 = None
        self.use_hint2 = None
        self.use_hint3 = None
        self.copy_hint1_btn.clicked.connect(self.set_hint1)
        self.copy_hint2_btn.clicked.connect(self.set_hint2)
        self.copy_hint3_btn.clicked.connect(self.set_hint3)
        self.clear_hint1_btn.clicked.connect(self.clear_hint1)
        self.clear_hint2_btn.clicked.connect(self.clear_hint2)
        self.clear_hint3_btn.clicked.connect(self.clear_hint3)
        self.clear_hints_btn.clicked.connect(self.clear_hints)

    def set_hint1(self):
        if self.hints_tv.model() is not None:
            index = self.hints_tv.currentIndex()
            hint = self.hints_tv.model().data(index)
            if hint is not None:
                self.hint1_le.setText(hint)
                self.update_query.prepare(f'UPDATE hints SET use = use + 1 WHERE text = "{hint}"')
                self.update_query.exec()
                self.db.commit()
                self.refresh_table()
                self.find_query.prepare(f'SELECT use FROM hints WHERE text = "{hint}"')
                self.find_query.exec()
                self.find_query.first()
                self.use_hint1 = self.find_query.value(0)

    def set_hint2(self):
        if self.hints_tv.model() is not None:
            index = self.hints_tv.currentIndex()
            hint = self.hints_tv.model().data(index)
            if hint is not None:
                self.hint2_le.setText(hint)
                self.update_query.prepare(f'UPDATE hints SET use = use + 1 WHERE text = "{hint}"')
                self.update_query.exec()
                self.db.commit()
                self.refresh_table()
                self.find_query.prepare(f'SELECT use FROM hints WHERE text = "{hint}"')
                self.find_query.exec()
                self.find_query.first()
                self.use_hint2 = self.find_query.value(0)

    def set_hint3(self):
        if self.hints_tv.model() is not None:
            index = self.hints_tv.currentIndex()
            hint = self.hints_tv.model().data(index)
            if hint is not None:
                self.hint3_le.setText(hint)
                self.update_query.prepare(f'UPDATE hints SET use = use + 1 WHERE text = "{hint}"')
                self.update_query.exec()
                self.db.commit()
                self.refresh_table()
                self.find_query.prepare(f'SELECT use FROM hints WHERE text = "{hint}"')
                self.find_query.exec()
                self.find_query.first()
                self.use_hint3 = self.find_query.value(0)

    def clear_hint1(self):
        self.hint1_le.clear()

    def clear_hint2(self):
        self.hint2_le.clear()

    def clear_hint3(self):
        self.hint3_le.clear()

    def clear_hints(self):
        self.hint1_le.clear()
        self.hint2_le.clear()
        self.hint3_le.clear()
        self.use_hint1 = None
        self.use_hint2 = None
        self.use_hint3 = None

    def choose_sql_model(self):
        self.load_query.clear()
        self.load_query.exec("SELECT text AS Подсказка FROM hints WHERE topic = 0 ORDER BY use, text")
        self.model.setQuery(self.load_query)
        self.hints_tv.resizeColumnToContents(0)
        self.hints_tv.verticalHeader().setVisible(False)
        self.hints_tv.show()

    def choose_python_model(self):
        self.load_query.clear()
        self.load_query.exec("SELECT text AS Подсказка FROM hints WHERE topic = 1 ORDER BY use, text")
        self.model.setQuery(self.load_query)
        self.hints_tv.resizeColumnToContents(0)
        self.hints_tv.verticalHeader().setVisible(False)
        self.hints_tv.show()

    def choose_js_model(self):
        self.load_query.clear()
        self.load_query.exec("SELECT text AS Подсказка FROM hints WHERE topic = 2 ORDER BY use, text")
        self.model.setQuery(self.load_query)
        self.hints_tv.resizeColumnToContents(0)
        self.hints_tv.verticalHeader().setVisible(False)
        self.hints_tv.show()

    def choose_html_model(self):
        self.load_query.clear()
        self.load_query.exec("SELECT text AS Подсказка FROM hints WHERE topic = 3 ORDER BY use, text")
        self.model.setQuery(self.load_query)
        self.hints_tv.resizeColumnToContents(0)
        self.hints_tv.verticalHeader().setVisible(False)
        self.hints_tv.show()

    def create_my_answer(self):
        text = '<hint1>\n' + self.hint1_le.text() + '\n</hint1>\n\n' + \
               '<hint2>\n' + self.hint2_le.text() + '\n</hint2>\n\n' + \
               '<hint3>\n' + self.hint3_le.text() + '\n</hint3>'
        self.answer_pte.clear()
        self.answer_pte.appendPlainText(text)

    def refresh_table(self):
        if self.sql_env_rb.isChecked():
            self.choose_sql_model()
        elif self.python_env_rb.isChecked():
            self.choose_python_model()
        elif self.js_env_rb.isChecked():
            self.choose_js_model()
        elif self.html_env_rb.isChecked():
            self.choose_html_model()

    def copy_my_answer(self):
        if (self.hint1_le.text().strip() == '' or
                self.hint2_le.text().strip() == '' or
                self.hint3_le.text().strip() == ''):
            msg = QMessageBox.critical(
                None,
                "Ошибка",
                "Должны быть заполнены все подсказки"
            )
            return
        if len({self.hint1_le.text().strip(),
                self.hint2_le.text().strip(),
                self.hint3_le.text().strip()}) < 3:
            msg = QMessageBox.critical(
                None,
                "Ошибка",
                "Подсказки должны отличаться"
            )
            return
        pyperclip.copy(self.answer_pte.toPlainText())
        topic = 0
        if self.sql_env_rb.isChecked():
            topic = 0
        elif self.python_env_rb.isChecked():
            topic = 1
        elif self.js_env_rb.isChecked():
            topic = 2
        elif self.html_env_rb.isChecked():
            topic = 3
        if self.use_hint1 is None:
            self.use_hint1 = 0
        if self.use_hint2 is None:
            self.use_hint2 = 0
        if self.use_hint3 is None:
            self.use_hint3 = 0
        self.add_query.exec(f'''INSERT INTO HINTS (TOPIC, TEXT, USE) VALUES ({topic}, "{self.hint1_le.text().strip()}", {self.use_hint1}),
                                ({topic}, "{self.hint2_le.text().strip()}", {self.use_hint2}),
                                ({topic}, "{self.hint3_le.text().strip()}", {self.use_hint3});''')
        self.db.commit()
        self.refresh_table()
        self.clear_hints()


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(tb)
    msg = QMessageBox.critical(
        None,
        "Error catched!:",
        tb
    )
    QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.excepthook = excepthook
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5', palette=qdarkstyle.DarkPalette))
    ex.show()
    sys.exit(app.exec_())
