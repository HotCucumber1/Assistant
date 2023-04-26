# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'handhelper_notes_window4.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_myNotesWindow(object):
    def setupUi(self, myNotesWindow):
        myNotesWindow.setObjectName("myNotesWindow")
        myNotesWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(myNotesWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        self.calendarWidget.setFont(font)
        self.calendarWidget.setObjectName("calendarWidget")
        self.verticalLayout.addWidget(self.calendarWidget)
        self.showOnlyEventsRadButton = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        self.showOnlyEventsRadButton.setFont(font)
        self.showOnlyEventsRadButton.setObjectName("showOnlyEventsRadButton")
        self.verticalLayout.addWidget(self.showOnlyEventsRadButton)
        self.showOnlyNotesRadButton = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        self.showOnlyNotesRadButton.setFont(font)
        self.showOnlyNotesRadButton.setObjectName("showOnlyNotesRadButton")
        self.verticalLayout.addWidget(self.showOnlyNotesRadButton)
        self.showBothRadButton = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        self.showBothRadButton.setFont(font)
        self.showBothRadButton.setObjectName("showBothRadButton")
        self.verticalLayout.addWidget(self.showBothRadButton)
        self.showCurrentDayButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        self.showCurrentDayButton.setFont(font)
        self.showCurrentDayButton.setObjectName("showCurrentDayButton")
        self.verticalLayout.addWidget(self.showCurrentDayButton)
        self.showAllnoteButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        self.showAllnoteButton.setFont(font)
        self.showAllnoteButton.setObjectName("showAllnoteButton")
        self.verticalLayout.addWidget(self.showAllnoteButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_2.addWidget(self.plainTextEdit)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.selectEventBox = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        self.selectEventBox.setFont(font)
        self.selectEventBox.setObjectName("selectEventBox")
        self.verticalLayout_2.addWidget(self.selectEventBox)
        self.showSelectedEventButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        self.showSelectedEventButton.setFont(font)
        self.showSelectedEventButton.setObjectName("showSelectedEventButton")
        self.verticalLayout_2.addWidget(self.showSelectedEventButton)
        self.saveAsFileButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        self.saveAsFileButton.setFont(font)
        self.saveAsFileButton.setObjectName("saveAsFileButton")
        self.verticalLayout_2.addWidget(self.saveAsFileButton)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        myNotesWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(myNotesWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        myNotesWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(myNotesWindow)
        self.statusbar.setObjectName("statusbar")
        myNotesWindow.setStatusBar(self.statusbar)

        self.retranslateUi(myNotesWindow)
        QtCore.QMetaObject.connectSlotsByName(myNotesWindow)

    def retranslateUi(self, myNotesWindow):
        _translate = QtCore.QCoreApplication.translate
        myNotesWindow.setWindowTitle(_translate("myNotesWindow", "Мои заметки"))
        self.showOnlyEventsRadButton.setText(_translate("myNotesWindow", "Показывать только события"))
        self.showOnlyNotesRadButton.setText(_translate("myNotesWindow", "Показывать только заметки"))
        self.showBothRadButton.setText(_translate("myNotesWindow", "Показывать события с замеками"))
        self.showCurrentDayButton.setText(_translate("myNotesWindow", "Показать на выбранный день"))
        self.showAllnoteButton.setText(_translate("myNotesWindow", "Показать все"))
        self.label.setText(_translate("myNotesWindow", "Показать только:"))
        self.showSelectedEventButton.setText(_translate("myNotesWindow", "Показать"))
        self.saveAsFileButton.setText(_translate("myNotesWindow", "Сохранить в файл"))