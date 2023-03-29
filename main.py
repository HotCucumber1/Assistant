# -*- coding: utf-8 -*-
import sys
import datetime as dt
import sqlite3
import csv

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox, QAction
from handhelper_main_window3 import Ui_MainWindow
from handhelper_notes_window4 import Ui_myNotesWindow
from handhelper_add_note_window2 import Ui_addNoteWidget
from handhelper_add_event_window4 import Ui_addeventWindow
from about_window import Ui_Form

from data import db_session
from data.events import Event
from data.notes import Note


# функция отображения окна с сообщением
def show_message(name, message_text):
    message = QMessageBox()
    if name == 'Ошибка':
        message.setWindowTitle('Ошибка')
        message.setIcon(QMessageBox.Warning)
    elif name == 'Успех':
        message.setWindowTitle('Сообщение')
        message.setIcon(QMessageBox.Information)
    elif name == 'Напоминание':
        message.setWindowTitle('Напоминание')
        message.setIcon(QMessageBox.Information)
    message.setText(message_text)
    message.setStandardButtons(QMessageBox.Ok)
    message.exec()


# классы-ошибки
class WrongEventNameError(Exception):
    pass


class EmptyEventError(Exception):
    pass


class Main(QMainWindow, Ui_MainWindow):  # главный экран
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect('./MyDB.db')  # подключение базы данных
        self.cursor = self.connection.cursor()
        self.today = dt.date.today()

        # вывод сообщения о сегодняшнем событии
        try:
            self.today_events = self.connection.cursor().execute(
                """SELECT event_name, time FROM events WHERE date = ?""",
                (str(self.today),))
            if bool(self.today_events):
                self.text = 'На сегодня запланированы:\n'
                for num, event in enumerate(self.today_events):
                    if event[1] is None:
                        self.text = self.text + f'{num + 1}) {event[0]}\n Время: весь день\n'
                    else:
                        self.text = self.text + f'{num + 1}) {event[0]}\n Время: {event[1]}\n'
                show_message('Напоминание', self.text)
        except Exception:
            show_message('Ошибка', 'Непредвиденная ошибка')
        self.initUi()

    def initUi(self):
        self.aboutAction = QAction('О приложении', self)
        self.aboutAction.triggered.connect(self.about)
        self.aboutMenu.addAction(self.aboutAction)

        self.showMyNoteButton.clicked.connect(self.show_my_note)
        self.addNewNoteButton.clicked.connect(self.add_new_note)
        self.addEventButton.clicked.connect(self.add_event)
        self.getEventsLikeTableButton.clicked.connect(self.get_events_like_table)

    def show_my_note(self):   # открыть окно со всеми событиями и заметками к ним
        self.note_window = NoteWindow(self, self.connection)
        self.note_window.show()

    def add_new_note(self):  # открыть окно с возможностью добавить заметку
        self.add_note_window = AddNoteWindow(self, self.connection)
        self.add_note_window.show()

    def add_event(self):  # открыть окно с возможностью добавить событие
        self.add_event_window = AddEventWindow(self, self.connection)
        self.add_event_window.show()

    def get_events_like_table(self):  # получить все события как таблицу (возможность сохранить как .csv файл)
        try:
            with open('Мои записи.csv', mode='w', newline='', encoding='utf-8') as table:
                writer = csv.writer(table, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                writer.writerow(['id', 'event', 'notes', 'date', 'time'])
                for event in db_sess.query(Event).all():
                    notes_text = ''
                    for note in db_sess.query(Note).filter(Note.event_id == event.id).all():
                        notes_text += note.note_name + '\n'

                    writer.writerow([event.id, event.event_name, notes_text, str(event.date), str(event.time)])

            show_message('Успех', 'Файл успешно сохранён')
        except Exception:
            show_message('Ошибка', 'Непредвиденная ошибка')

    def about(self):  # показать окно с описанием приложения
        self.about_window = About(self)
        self.about_window.show()

    def closeEvent(self, event):
        self.connection.close()


class NoteWindow(QMainWindow, Ui_myNotesWindow):  # окно поиска (навигации) по заметкам и событиям к ним
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.connection = args[-1]
        self.cursor = self.connection.cursor()

        self.result = self.cursor.execute("""SELECT event_name FROM events""").fetchall()
        self.selectEventBox.addItems([''.join(i).rstrip('\n') for i in self.result])

        self.showCurrentDayButton.clicked.connect(self.show_current_day)
        self.showAllnoteButton.clicked.connect(self.show_all_note)
        self.showSelectedEventButton.clicked.connect(self.show_selected)
        self.saveAsFileButton.clicked.connect(self.save_as_file)

        self.showBothRadButton.setChecked(True)

    def show_current_day(self):  # показать события на выбранный день
        try:
            self.plainTextEdit.clear()
            self.current_date = self.calendarWidget.selectedDate().toPyDate()
            if self.showOnlyEventsRadButton.isChecked(): # если выбрано "Показывать только события"
                self.events = self.cursor.execute("""SELECT event_name FROM events WHERE date = ?""",
                                              (str(self.current_date),)).fetchall()
                self.events = [''.join(i) for i in self.events]
                if len(self.events) == 0:
                    self.plainTextEdit.appendPlainText("На этот день событий нет")
                else:
                    for num, event in enumerate(self.events):
                        self.plainTextEdit.appendPlainText(f"{num + 1}) {event}")
                        self.plainTextEdit.appendPlainText(f'    Дата: {str(self.current_date)}')
                        self.event_time = self.cursor.execute(
                            """SELECT time FROM events WHERE event_name = ?""", (event,)).fetchone()
                        if self.event_time[0] is None:
                            self.plainTextEdit.appendPlainText(f'    Время: весь день')
                        else:
                            self.plainTextEdit.appendPlainText(f'    Время: {self.event_time[0]}')
                        self.plainTextEdit.appendPlainText('')

            elif self.showOnlyNotesRadButton.isChecked():  # если выбрано "Показывать только заметки"
                self.notes = self.cursor.execute("""SELECT note_name FROM notes 
                                                    WHERE event IN (SELECT id FROM events WHERE date = ?)""",
                                                (str(self.current_date),)).fetchall()
                self.notes = [i[0] for i in self.notes]

                if len(self.notes) == 0:
                    self.plainTextEdit.appendPlainText("На этот день заметок нет")
                else:
                    for num, note in enumerate(self.notes):
                        self.plainTextEdit.appendPlainText(f"{num + 1}) {note}")

            elif self.showBothRadButton.isChecked():  # если выбрано "Показывать всё"
                self.events = self.cursor.execute("""SELECT id, event_name FROM events WHERE date = ?""",
                                                (str(self.current_date),)).fetchall()
                if bool(self.events):
                    for num, event in enumerate(self.events):
                        self.notes = self.cursor.execute(f"""SELECT note_name FROM notes WHERE event = ?""",
                                                        (event[0],))
                        self.notes = [''.join(i) for i in self.notes]

                        self.plainTextEdit.appendPlainText(f"{num + 1}) {event[1]}")
                        self.plainTextEdit.appendPlainText(f'    Дата: {str(self.current_date)}')
                        self.event_time = self.cursor.execute(
                            """SELECT time FROM events WHERE event_name = ?""", (event[1],)).fetchone()
                        if self.event_time[0] is None:
                            self.plainTextEdit.appendPlainText(f'    Время: весь день')
                        else:
                            self.plainTextEdit.appendPlainText(f'    Время: {self.event_time[0]}')

                        for note in self.notes:
                            self.plainTextEdit.appendPlainText(f'    *{note}')
                        self.plainTextEdit.appendPlainText('')
                else:
                    self.plainTextEdit.appendPlainText('На этот день событий нет')

        except Exception:
            show_message('Ошибка', 'Непредвиденная ошибка')

    def show_all_note(self):  # показать все события со всеми заметками
        try:
            self.events = self.cursor.execute("""SELECT id, event_name, date, time FROM events""").fetchall()
            for num, event in enumerate(self.events):
                self.notes = self.cursor.execute(f"""SELECT note_name FROM notes WHERE event = ?""",
                                                (event[0],))
                self.notes = [''.join(i) for i in self.notes]

                self.plainTextEdit.appendPlainText(f"{num + 1}) {event[1]}")
                self.plainTextEdit.appendPlainText(f'    Дата: {event[2]}')

                if event[3] is None:
                    self.plainTextEdit.appendPlainText(f'    Время: весь день')
                else:
                    self.plainTextEdit.appendPlainText(f'    Время: {event[3]}')

                for note in self.notes:
                    self.plainTextEdit.appendPlainText(f'    *{note}')
                self.plainTextEdit.appendPlainText('')
        except Exception:
            show_message('Ошибка', 'Непредвиденная ошибка')

    def show_selected(self):  # показать только выбранное событие
        try:
            self.plainTextEdit.clear()

            self.event = self.cursor.execute("""SELECT id, date, time FROM events WHERE event_name = ?""",
                                            (self.selectEventBox.currentText(),)).fetchone()
            self.notes = self.cursor.execute("""SELECT note_name FROM notes WHERE event = ?""",
                                            (self.event[0],)).fetchall()
            self.notes = [''.join(i) for i in self.notes]
            self.plainTextEdit.appendPlainText(self.selectEventBox.currentText())
            self.plainTextEdit.appendPlainText(f'    Дата: {self.event[1]}')
            if self.event[2] is None:
                self.plainTextEdit.appendPlainText(f'    Время: весь день')
            else:
                self.plainTextEdit.appendPlainText(f'    Время: {self.event[2]}')

            for note in self.notes:
                self.plainTextEdit.appendPlainText(f'    *{note}')
        except Exception:
            show_message('Ошибка', 'Непредвиденная ошибка')

    def save_as_file(self):  # сохранить то, что показано как файл.txt
        try:
            if self.showBothRadButton.isChecked():
                with open('Мои записи.txt', mode='w', encoding='utf-8') as file:
                    file.write(self.plainTextEdit.toPlainText())
            elif self.showOnlyNotesRadButton.isChecked():
                with open('Мои заметки', mode='w', encoding='utf-8') as file:
                    file.write(self.plainTextEdit.toPlainText())
            elif self.showOnlyEventsRadButton.isChecked():
                with open('Мои события', mode='w', encoding='utf-8') as file:
                    file.write(self.plainTextEdit.toPlainText())
            show_message('Успех', 'Файл успешно сохранён')
        except Exception:
            show_message('Ошибка', 'Непредвиденная ошибка')


class AddNoteWindow(QWidget, Ui_addNoteWidget):  # окно добавления заметки
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.connection = args[-1]
        self.cursor = self.connection.cursor()
        self.result = self.cursor.execute("""SELECT event_name FROM events""").fetchall()
        self.chooseEventBox.addItems([''.join(i).rstrip('\n') for i in self.result])

        self.addIt.clicked.connect(self.add_note)

    def add_note(self):  # добавить написанное как заметку
        try:
            self.event = self.cursor.execute("""SELECT id FROM events WHERE event_name = ?""",
                                             (self.chooseEventBox.currentText(),)).fetchone()
            self.note_text = self.plainTextEdit.toPlainText().rstrip('\n')
            if self.note_text == '':
                raise EmptyEventError
            self.result = self.cursor.execute("""INSERT INTO notes (note_name, event) VALUES (?, ?)""",
                                              (self.note_text, self.event[0]))

            self.result = self.cursor.execute("""UPDATE events SET number_of_notes = number_of_notes + 1 
                                                WHERE event_name = ?""", (self.chooseEventBox.currentText(),))
            self.connection.commit()
            show_message('Успех', 'Заметка успешно сохранена')
        except EmptyEventError:
            show_message('Ошибка', 'Пустая заметка')
        except Exception:
            show_message('Ошибка', 'Непредвиденная ошибка')


class AddEventWindow(QWidget, Ui_addeventWindow):  # окно добавления события
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.connection = args[-1]
        self.cursor = self.connection.cursor()
        self.addIt.clicked.connect(self.add_event)

    def add_event(self):  # добавить событие с выбранными датой и временем
        try:
            self.date = self.calendarWidget.selectedDate().toPyDate()
            self.time = self.timeEdit.time().toPyTime()
            self.event_name = self.plainTextEdit.toPlainText().rstrip('\n')
            self.we_have = self.cursor.execute("""SELECT event_name FROM events""").fetchall()

            if str(self.event_name) == '':
                raise EmptyEventError
            elif str(self.event_name) in [''.join(i).rstrip('\n') for i in self.we_have]:
                raise WrongEventNameError
            if self.withoutTimeBox.isChecked():
                self.result = self.cursor.execute("""INSERT INTO events(event_name, number_of_notes, date, time)
                                                    VALUES (?, ?, ?, ?)""",
                                                    (str(self.event_name), 0, str(self.date), None))
            else:
                self.result = self.cursor.execute("""INSERT INTO events(event_name, number_of_notes, date, time)
                                                    VALUES (?, ?, ?, ?)""",
                                                    (str(self.event_name), 0, str(self.date), str(self.time)))
            self.connection.commit()
            show_message('Успех', 'Событие успешно сохранено')

        except EmptyEventError:
            show_message('Ошибка', 'Пустое событие')
        except WrongEventNameError:
            show_message('Ошибка', 'Событие с таким именем уже существует')
        except Exception:
            show_message('Ошибка', 'Непредвиденная ошибка')


class About(QWidget, Ui_Form):  # окно с информацией о приложении
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    db_session.global_init("db/new_events_db.db")
    db_sess = db_session.create_session()

    app = QApplication(sys.argv)
    wnd = Main()
    wnd.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
