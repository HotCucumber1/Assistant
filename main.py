# -*- coding: utf-8 -*-
import sys
import datetime as dt
import csv

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox, QAction

from interface.py_files.handhelper_main_window3 import Ui_MainWindow
from interface.py_files.handhelper_notes_window4 import Ui_myNotesWindow
from interface.py_files.handhelper_add_note_window2 import Ui_addNoteWidget
from interface.py_files.handhelper_add_event_window4 import Ui_addeventWindow
from interface.py_files.about_window import Ui_Form

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
        self.today = dt.date.today()

        # вывод сообщения о сегодняшнем событии
        try:
            today_events = db_sess.query(Event).filter(Event.date == self.today)

            if list(today_events):
                self.text = 'На сегодня запланированы:\n'
                num = 1
                for event in today_events:
                    if event.time is None:
                        time = "весь день\n"
                    else:
                        time = event.time.strftime("%H:%M")
                    self.text += f"{num}) {event.event_name}\n    Время: {time}"
                    num += 1

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
        self.note_window = NoteWindow(self)
        self.note_window.show()

    def add_new_note(self):  # открыть окно с возможностью добавить заметку
        self.add_note_window = AddNoteWindow(self)
        self.add_note_window.show()

    def add_event(self):  # открыть окно с возможностью добавить событие
        self.add_event_window = AddEventWindow(self)
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


class NoteWindow(QMainWindow, Ui_myNotesWindow):  # окно поиска (навигации) по заметкам и событиям к ним
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)

        self.result = db_sess.query(Event).all()
        self.selectEventBox.addItems([''.join(i.event_name).rstrip('\n') for i in self.result])

        self.showCurrentDayButton.clicked.connect(self.show_current_day)
        self.showAllnoteButton.clicked.connect(self.show_all_note)
        self.showSelectedEventButton.clicked.connect(self.show_selected)
        self.saveAsFileButton.clicked.connect(self.save_as_file)

        self.showBothRadButton.setChecked(True)

    def show_current_day(self):  # показать события на выбранный день
        try:
            self.plainTextEdit.clear()
            self.current_date = self.calendarWidget.selectedDate().toPyDate()
            self.events = db_sess.query(Event).filter(Event.date == self.current_date)
            self.notes = db_sess.query(Note).filter(Note.event_id.in_([event.id for event in self.events]))

            if self.showOnlyEventsRadButton.isChecked():  # если выбрано "Показывать только события"

                if not list(self.events):
                    self.plainTextEdit.appendPlainText("На этот день событий нет")
                else:
                    num = 1
                    for event in self.events:
                        self.plainTextEdit.appendPlainText(f"{num}) {event.event_name}")
                        self.plainTextEdit.appendPlainText(f'    Дата: {str(self.current_date)}')
                        if event.time is None:
                            self.plainTextEdit.appendPlainText(f'    Время: весь день')
                        else:
                            self.plainTextEdit.appendPlainText(f'    Время: {event.time.strftime("%H:%M")}')
                        num += 1
                    self.plainTextEdit.appendPlainText('')

            elif self.showOnlyNotesRadButton.isChecked():  # если выбрано "Показывать только заметки"

                if not list(self.notes):
                    self.plainTextEdit.appendPlainText("На этот день заметок нет")
                else:
                    num = 1
                    for note in self.notes:
                        self.plainTextEdit.appendPlainText(f"{num}) {note.note_name}")
                        num += 1

            elif self.showBothRadButton.isChecked():  # если выбрано "Показывать всё"

                if list(self.events):
                    num = 1
                    for event in self.events:
                        self.plainTextEdit.appendPlainText(f"{num}) {event.event_name}")
                        self.plainTextEdit.appendPlainText(f'    Дата: {str(self.current_date)}')
                        if event.time is None:
                            self.plainTextEdit.appendPlainText(f'    Время: весь день')
                        else:
                            self.plainTextEdit.appendPlainText(f'    Время: {event.time.strftime("%H:%M")}')

                        if self.notes:
                            for note in self.notes:
                                self.plainTextEdit.appendPlainText(f'    *{note.note_name}')
                        self.plainTextEdit.appendPlainText('')
                        num += 1
                else:
                    self.plainTextEdit.appendPlainText('На этот день событий нет')

        except Exception:
            show_message('Ошибка', 'Непредвиденная ошибка')

    def show_all_note(self):  # показать все события со всеми заметками
        try:
            self.plainTextEdit.clear()
            if list(self.result):
                num = 1
                for event in self.result:
                    self.nots = db_sess.query(Note).filter(Note.event_id == event.id)
                    self.plainTextEdit.appendPlainText(f"{num}) {event.event_name}")
                    self.plainTextEdit.appendPlainText(f'    Дата: {str(event.date)}')

                    if event.time is None:
                        self.plainTextEdit.appendPlainText(f'    Время: весь день')
                    else:
                        self.plainTextEdit.appendPlainText(f'    Время: {event.time.strftime("%H:%M")}')

                    if self.nots:
                        for note in self.nots:
                            self.plainTextEdit.appendPlainText(f'    *{note.note_name}')
                    self.plainTextEdit.appendPlainText('')
                    num += 1
            else:
                self.plainTextEdit.appendPlainText('Событий нет')

        except Exception:
            show_message('Ошибка', 'Непредвиденная ошибка')

    def show_selected(self):  # показать только выбранное событие
        try:
            self.plainTextEdit.clear()

            self.event = db_sess.query(Event).filter(Event.event_name == self.selectEventBox.currentText()).first()
            self.note = db_sess.query(Note).filter(Note.event_id == self.event.id)

            self.plainTextEdit.appendPlainText(f"{self.event.event_name}")
            self.plainTextEdit.appendPlainText(f'    Дата: {str(self.event.date)}')
            if self.event.time is None:
                self.plainTextEdit.appendPlainText(f'    Время: весь день')
            else:
                self.plainTextEdit.appendPlainText(f'    Время: {self.event.time.strftime("%H:%M")}')

            for note in self.note:
                self.plainTextEdit.appendPlainText(f'    *{note.note_name}')

        except Exception:
            show_message('Ошибка', 'Непредвиденная ошибка')

    def save_as_file(self):  # сохранить то, что показано как файл.txt
        try:
            if self.showBothRadButton.isChecked():
                file_name = "Мои записи.txt"

            elif self.showOnlyNotesRadButton.isChecked():
                file_name = "Мои заметки.txt"

            elif self.showOnlyEventsRadButton.isChecked():
                file_name = "Мои события.txt"

            with open(file_name, mode='w', encoding='utf-8') as file:
                file.write(self.plainTextEdit.toPlainText())
            show_message('Успех', 'Файл успешно сохранён')
        except Exception:
            show_message('Ошибка', 'Непредвиденная ошибка')


class AddNoteWindow(QWidget, Ui_addNoteWidget):  # окно добавления заметки
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.chooseEventBox.addItems([i.event_name for i in db_sess.query(Event)])
        self.addIt.clicked.connect(self.add_note)

    def add_note(self):  # добавить написанное как заметку
        try:
            self.event = db_sess.query(Event).filter(Event.event_name == self.chooseEventBox.currentText()).first().id
            self.note_text = self.plainTextEdit.toPlainText().rstrip('\n')

            if self.note_text == '':
                raise EmptyEventError

            note = Note()
            note.note_name = self.note_text
            note.event_id = self.event

            update = db_sess.query(Event).filter(Event.id == self.event).first()
            update.number_of_notes += 1

            db_sess.add(note)
            db_sess.commit()
            show_message('Успех', 'Заметка успешно сохранена')

        except EmptyEventError:
            show_message('Ошибка', 'Пустая заметка')
        except Exception:
            show_message('Ошибка', 'Непредвиденная ошибка')


class AddEventWindow(QWidget, Ui_addeventWindow):  # окно добавления события
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.addIt.clicked.connect(self.add_event)

    def add_event(self):  # добавить событие с выбранными датой и временем
        try:
            self.date = self.calendarWidget.selectedDate().toPyDate()
            self.time = self.timeEdit.time().toPyTime()
            self.event_name = self.plainTextEdit.toPlainText().rstrip('\n')

            self.we_have = [event.event_name for event in db_sess.query(Event)]
            if str(self.event_name) == '':
                raise EmptyEventError
            elif str(self.event_name) in self.we_have:
                raise WrongEventNameError

            event = Event()
            event.event_name = self.event_name
            event.number_of_notes = 0
            event.date = self.date

            if self.withoutTimeBox.isChecked():
                event.time = None
            else:
                event.time = self.time
            db_sess.add(event)
            db_sess.commit()

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
