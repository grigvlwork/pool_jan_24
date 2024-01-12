import sys
import traceback
import subprocess
import pyperclip
import black
import sys
import re
import enchant
import difflib
import datetime
import time
import shutil
import os
import glob
import qdarkstyle
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QFileDialog
from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from mainwindow import Ui_MainWindow
import requests
import winreg
from file_proc import Files


def remove_comments(code):
    return re.sub(r'#.*', '', code)


def get_download_path():
    if os.name == 'nt':
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')


def spell_check(text):
    rus_alph = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    words = []
    word = ''
    for c in text:
        if c.lower() in rus_alph:
            word += c
        else:
            if len(word) > 0:
                words.append(word)
                word = ''
    if len(word) > 0 and word not in words:
        words.append(word)
    result = []
    dictionary = enchant.Dict("ru_RU")
    for w in words:
        if not dictionary.check(w):
            sim = dict()
            suggestions = set(dictionary.suggest(w))
            for word in suggestions:
                measure = difflib.SequenceMatcher(None, w, word).ratio()
                sim[measure] = word
            try:
                result.append([w, sim[max(sim.keys())]])
            except Exception:
                pass
    return result


def check_dict():
    file1 = '/_venv/Lib/site-packages/enchant/data/mingw64/share/enchant/hunspell/ru_RU.aff'
    file2 = '/_venv/Lib/site-packages/enchant/data/mingw64/share/enchant/hunspell/ru_RU.dic'
    file_path1 = os.getcwd() + '/venv/Lib/site-packages/enchant/data/mingw64/share/enchant/hunspell/ru_RU.aff'
    file_path2 = os.getcwd() + '/venv/Lib/site-packages/enchant/data/mingw64/share/enchant/hunspell/ru_RU.dic'
    file_path = os.getcwd() + '/venv/Lib/site-packages/enchant/data/mingw64/share/enchant/hunspell/'
    try:
        if (not os.path.exists(file_path1)) or (not os.path.exists(file_path2)):
            for file in glob.glob(os.getcwd() + file1):
                shutil.copy(file, file_path)
            for file in glob.glob(os.getcwd() + file2):
                shutil.copy(file, file_path)
        return True
    except Exception:
        return False


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.explanation_text = ''
        self.result_run = ''
        self.answer_number = 0
        self.allow_spell_check = check_dict()
        self.correct_code_model = QStandardItemModel()
        self.explanation_pte.textChanged.connect(self.explanation_changed)
        self.run_btn.clicked.connect(self.run_correct)
        self.toggle_theme_btn.clicked.connect(self.change_theme)
        self.pep8_btn.clicked.connect(self.pep8_correct)
        self.paste_btn.clicked.connect(self.paste_code)
        self.paste_explanation_btn.clicked.connect(self.paste_explanation)
        self.correct_tw.currentChanged.connect(self.correct_row_generator)
        self.copy_answer_btn.clicked.connect(self.copy_my_answer)
        self.clear_btn.clicked.connect(self.clear_explanation)
        self.setWindowTitle(f'Пул январь 2024 {self.check_version()}')
        self.link_to_task_le.textChanged.connect(self.link_to_task_changed)
        self.link_pb.clicked.connect(self.insert_link)
        self.my_error_txt = ''
        self.files = None
        self.file_name = None
        # https://dev.to/ashishpandey/say-goodbye-to-chrome-build-your-own-browser-with-pyqt5-and-python-23ld

    def insert_link(self):
        self.link_to_task_le.setText(pyperclip.paste())

    def link_to_task_changed(self):
        if self.files is None:
            self.files = Files()
        if len(self.link_to_task_le.text()) > 0:
            id = self.files.get_id_from_url(self.link_to_task_le.text())
            code = self.correct_code_pte.toPlainText()
            file_name = self.files.get_filename_from_code(code)
            if file_name != '':
                if self.files.local_files is not None and id in self.files.local_files \
                        and self.files.get_local_file(id, file_name) == 1:
                    QMessageBox.information(self,
                                            'Информация', 'Файл скопирован в папку программы',
                                            QMessageBox.Ok)
                elif self.files.global_files is not None and id in self.files.global_files \
                        and self.files.get_global_file(id, file_name) == 1:
                    QMessageBox.information(self,
                                            'Информация', 'Файл скопирован в папку программы',
                                            QMessageBox.Ok)
                else:
                    QMessageBox.information(self,
                                            'Информация', 'Файл не найден в локальных папках и на сетевом диске,\n' +
                                            ' скачайте его и нажмите ОК для выбора',
                                            QMessageBox.Ok)
                    filename, ok = QFileDialog.getOpenFileName(
                        None, 'Выбор файла', get_download_path(), 'Файлы данных к задачам (*.txt *.csv)', None
                    )
                    if filename:
                        if self.files.save_file(id, filename) == 1:
                            if self.files.get_local_file(id, os.path.basename(filename)) == 1:
                                QMessageBox.information(self,
                                                        'Информация', 'Файл скопирован в папку программы',
                                                        QMessageBox.Ok)

    def run_text(self, text, timeout):
        with open('code.py', 'w', encoding='utf-8') as c:
            c.write(text)
        try:
            completed_process = subprocess.run(['python', 'code.py'], capture_output=True, text=True, timeout=timeout)
            if completed_process.returncode == 0:
                t = completed_process.stdout
                t = t.encode('cp1251').decode('utf-8')
                self.result_run = t
                if len(t) > 50:
                    return t[:50] + '..'
                else:
                    return t
            else:
                t = completed_process.stderr
                t = t.encode('cp1251').decode('utf-8')
                self.my_error_txt = t
                self.result_run = t
                # if len(t) > 50:
                #     return t[:150] + '\n' + t[150:]
                # else:
                return t
        except subprocess.TimeoutExpired:
            return f'Программа выполнялась более {timeout} секунд'

    def check_version(self):
        v = None
        try:
            with open('version.txt') as f:
                v = f.read().strip()
        except Exception as e:
            print(str(e))
        if v is not None:
            try:
                r = requests.get('https://github.com/grigvlwork/pool_jan_24/blob/main/version.txt')
                new_v = r.text[r.text.find("rawLines") + 12:r.text.find("rawLines") + 17]
                if v != new_v:
                    QMessageBox.information(self,
                                            'Информация', f'Вышла новая версия {new_v}\nОбновите программу',
                                            QMessageBox.Ok)
            except Exception as e:
                print(str(e))
            return v
        return ''

    def clear_explanation(self):
        self.explanation_text = ''
        self.explanation_pte.clear()

    def change_theme(self):
        if self.toggle_theme_btn.text() == 'Светлая тема':
            self.toggle_theme_btn.setText('Тёмная тема')
            app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5', palette=qdarkstyle.LightPalette))
        else:
            self.toggle_theme_btn.setText('Светлая тема')
            app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5', palette=qdarkstyle.DarkPalette))

    def run_correct(self):
        code = self.correct_code_pte.toPlainText()
        timeout = self.timeout_sb.value()
        self.correct_output_lb.setText('Вывод: ' + self.run_text(remove_comments(code), timeout))
        self.correct_output_lb.setToolTip(self.result_run)

    def explanation_changed(self):
        self.explanation_text = self.explanation_pte.toPlainText()
        self.set_my_answer()

    def pep8_correct(self):
        self.correct_code_pte.setPlainText(self.correct_code_pte.toPlainText().replace('\t', '    '))
        code = self.correct_code_pte.toPlainText()
        try:
            code = black.format_str(code, mode=black.Mode(
                target_versions={black.TargetVersion.PY310},
                line_length=101,
                string_normalization=False,
                is_pyi=False,
            ), )
        except Exception as err:
            code = code.strip()
        self.correct_code_pte.setPlainText(code)
        self.correct_code = code

    def copy_my_answer(self):
        if self.allow_spell_check:
            errors = spell_check(self.explanation_pte.toPlainText())
            if self.allow_spell_check and len(errors) > 0 or self.explanation_pte.toPlainText().count('```') % 2 != 0 \
                    or self.explanation_pte.toPlainText().count('`') % 2 != 0:
                s = 'Обнаружены ошибки в тексте, всё равно скопировать?\n'
                for err in errors:
                    s += err[0] + ':    ' + err[1] + '\n'
                if self.explanation_pte.toPlainText().count('```') % 2 != 0 \
                        or self.explanation_pte.toPlainText().count('`') % 2 != 0:
                    s += 'Непарное количество бэктиков'
                message = QMessageBox.question(self, "Орфографические ошибки", s,
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if message != QMessageBox.Yes:
                    return
        if self.explanation_pte.toPlainText().count('```') % 2 != 0:
            message = QMessageBox.question(self, "Ошибки", 'Непарное количество бэктиков',
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        pyperclip.copy(self.my_answer_pte.toPlainText())

    def correct_row_generator(self):
        if self.correct_tw.currentIndex() == 1:
            self.correct_code_model.clear()
            for row in self.correct_code_pte.toPlainText().split('\n'):
                it = QStandardItem(row)
                self.correct_code_model.appendRow(it)
            self.correct_code_tv.setModel(self.correct_code_model)
            self.correct_code_tv.horizontalHeader().setVisible(False)
            self.correct_code_tv.resizeColumnToContents(0)

    def paste_code(self):
        self.correct_code_pte.clear()
        self.correct_code_pte.appendPlainText(pyperclip.paste())

    def paste_explanation(self):
        self.explanation_pte.clear()
        self.explanation_pte.appendPlainText(pyperclip.paste())

    def set_my_answer(self):
        if self.err_cb.isChecked():
            self.my_answer_pte.setPlainText(f'<my_error>\n{self.my_error_txt}\n</my_error>\n' +
                                            self.explanation_text)
        else:
            self.my_answer_pte.setPlainText(self.explanation_text)


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
