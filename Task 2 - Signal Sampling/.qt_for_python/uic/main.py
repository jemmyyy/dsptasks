# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from pyqtgraph import PlotWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1660, 740)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame_14 = QFrame(self.frame)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setGeometry(QRect(10, 10, 741, 601))
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.frame_15 = QFrame(self.frame_14)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setGeometry(QRect(10, 560, 721, 31))
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.Save_textEdit = QTextEdit(self.frame_15)
        self.Save_textEdit.setObjectName(u"Save_textEdit")
        self.Save_textEdit.setGeometry(QRect(570, 5, 141, 21))
        self.SaveButton = QPushButton(self.frame_15)
        self.SaveButton.setObjectName(u"SaveButton")
        self.SaveButton.setGeometry(QRect(480, 5, 75, 23))
        self.SaveButton.setStyleSheet(u"QPushButton\n"
"{\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-color: black;\n"
"    font: 9pt \"Century\";\n"
"}")
        self.ConfirmButton = QPushButton(self.frame_15)
        self.ConfirmButton.setObjectName(u"ConfirmButton")
        self.ConfirmButton.setGeometry(QRect(390, 5, 75, 23))
        self.ConfirmButton.setStyleSheet(u"QPushButton\n"
"{\n"
"   border-style: outset;\n"
"    border-width: 2px;\n"
"    border-color: black;\n"
"    font: 9pt \"Century\";\n"
"}")
        self.horizontalSlider = QSlider(self.frame_15)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setGeometry(QRect(10, 5, 341, 20))
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.splitter_10 = QSplitter(self.frame_14)
        self.splitter_10.setObjectName(u"splitter_10")
        self.splitter_10.setGeometry(QRect(10, 10, 721, 541))
        self.splitter_10.setOrientation(Qt.Horizontal)
        self.splitter_11 = QSplitter(self.splitter_10)
        self.splitter_11.setObjectName(u"splitter_11")
        self.splitter_11.setOrientation(Qt.Vertical)
        self.plotGraphicsView = PlotWidget(self.splitter_11)
        self.plotGraphicsView.setObjectName(u"plotGraphicsView")
        self.splitter_11.addWidget(self.plotGraphicsView)
        self.reconstructGraphicsView = PlotWidget(self.splitter_11)
        self.reconstructGraphicsView.setObjectName(u"reconstructGraphicsView")
        self.splitter_11.addWidget(self.reconstructGraphicsView)
        self.splitter_10.addWidget(self.splitter_11)
        self.splitter_12 = QSplitter(self.splitter_10)
        self.splitter_12.setObjectName(u"splitter_12")
        self.splitter_12.setOrientation(Qt.Vertical)
        self.ComposergraphicsView = PlotWidget(self.splitter_12)
        self.ComposergraphicsView.setObjectName(u"ComposergraphicsView")
        self.splitter_12.addWidget(self.ComposergraphicsView)
        self.graphicsView_3 = PlotWidget(self.splitter_12)
        self.graphicsView_3.setObjectName(u"graphicsView_3")
        self.splitter_12.addWidget(self.graphicsView_3)
        self.splitter_10.addWidget(self.splitter_12)
        self.frame_16 = QFrame(self.frame)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setGeometry(QRect(760, 10, 491, 271))
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.frame_17 = QFrame(self.frame_16)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setGeometry(QRect(220, 10, 261, 161))
        self.frame_17.setFrameShape(QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.AmplitudeLine = QLineEdit(self.frame_17)
        self.AmplitudeLine.setObjectName(u"AmplitudeLine")
        self.AmplitudeLine.setGeometry(QRect(10, 40, 91, 20))
        self.FrequencyLine = QLineEdit(self.frame_17)
        self.FrequencyLine.setObjectName(u"FrequencyLine")
        self.FrequencyLine.setGeometry(QRect(10, 70, 91, 20))
        self.lineEdit_8 = QLineEdit(self.frame_17)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setGeometry(QRect(10, 100, 91, 20))
        self.Amplitude_textEdit = QTextEdit(self.frame_17)
        self.Amplitude_textEdit.setObjectName(u"Amplitude_textEdit")
        self.Amplitude_textEdit.setGeometry(QRect(110, 40, 141, 21))
        self.Frequency_textEdit = QTextEdit(self.frame_17)
        self.Frequency_textEdit.setObjectName(u"Frequency_textEdit")
        self.Frequency_textEdit.setGeometry(QRect(110, 70, 141, 21))
        self.Phase_Shift_textEdit = QTextEdit(self.frame_17)
        self.Phase_Shift_textEdit.setObjectName(u"Phase_Shift_textEdit")
        self.Phase_Shift_textEdit.setGeometry(QRect(110, 100, 141, 21))
        self.lineEdit_9 = QLineEdit(self.frame_17)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        self.lineEdit_9.setGeometry(QRect(10, 10, 91, 20))
        self.SignalcomboBox = QComboBox(self.frame_17)
        self.SignalcomboBox.addItem("")
        self.SignalcomboBox.addItem("")
        self.SignalcomboBox.setObjectName(u"SignalcomboBox")
        self.SignalcomboBox.setGeometry(QRect(110, 10, 141, 26))
        self.ApplyButton = QPushButton(self.frame_17)
        self.ApplyButton.setObjectName(u"ApplyButton")
        self.ApplyButton.setGeometry(QRect(10, 130, 91, 23))
        self.ApplyButton.setStyleSheet(u"QPushButton\n"
"{\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-color: black;\n"
"    font: 9pt \"Century\";\n"
"}")
        self.AddButton = QPushButton(self.frame_17)
        self.AddButton.setObjectName(u"AddButton")
        self.AddButton.setGeometry(QRect(110, 130, 75, 23))
        self.AddButton.setStyleSheet(u"QPushButton\n"
"{\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-color: black;\n"
"    font: 9pt \"Century\";\n"
"}")
        self.DeletecomboBox = QComboBox(self.frame_16)
        self.DeletecomboBox.setObjectName(u"DeletecomboBox")
        self.DeletecomboBox.setGeometry(QRect(170, 190, 311, 28))
        self.DeletecomboBox.setStyleSheet(u" QComboBox\n"
"{\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-color: black;\n"
"    font: 9pt \"Century\";\n"
"}")
        self.DeleteButton = QPushButton(self.frame_16)
        self.DeleteButton.setObjectName(u"DeleteButton")
        self.DeleteButton.setGeometry(QRect(30, 190, 111, 28))
        self.DeleteButton.setStyleSheet(u"QPushButton\n"
"{\n"
"   border-style: outset;\n"
"    border-width: 2px;\n"
"    border-color: black;\n"
"    font: 9pt \"Century\";\n"
"}")
        self.BrowseButton = QPushButton(self.frame_16)
        self.BrowseButton.setObjectName(u"BrowseButton")
        self.BrowseButton.setGeometry(QRect(70, 20, 101, 31))
        self.BrowseButton.setStyleSheet(u"QPushButton\n"
"{\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-color: black;\n"
"    font: 9pt \"Century\";\n"
"}")
        self.ShowButton = QPushButton(self.frame_16)
        self.ShowButton.setObjectName(u"ShowButton")
        self.ShowButton.setGeometry(QRect(70, 60, 101, 31))
        self.ShowButton.setStyleSheet(u"QPushButton\n"
"{\n"
"   border-style: outset;\n"
"    border-width: 2px;\n"
"    border-color: black;\n"
"    font: 9pt \"Century\";\n"
"}")
        self.HideButton = QPushButton(self.frame_16)
        self.HideButton.setObjectName(u"HideButton")
        self.HideButton.setGeometry(QRect(70, 100, 101, 31))
        self.HideButton.setStyleSheet(u"QPushButton\n"
"{\n"
"   border-style: outset;\n"
"    border-width: 2px;\n"
"    border-color: black;\n"
"    font: 9pt \"Century\";\n"
"}")

        self.verticalLayout.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1660, 22))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.SaveButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Press to Save</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.SaveButton.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(tooltip)
        self.ConfirmButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Press to Confirm</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.ConfirmButton.setText(QCoreApplication.translate("MainWindow", u"Confirm", None))
        self.AmplitudeLine.setText(QCoreApplication.translate("MainWindow", u"Amplitude", None))
        self.FrequencyLine.setText(QCoreApplication.translate("MainWindow", u"Frequency", None))
        self.lineEdit_8.setText(QCoreApplication.translate("MainWindow", u" Phase_Shift", None))
        self.lineEdit_9.setText(QCoreApplication.translate("MainWindow", u"Signal ", None))
        self.SignalcomboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Sine Signal", None))
        self.SignalcomboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Cosine Signal", None))

#if QT_CONFIG(tooltip)
        self.ApplyButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Press to Show Signal </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.ApplyButton.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
#if QT_CONFIG(tooltip)
        self.AddButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Press to Add Signal </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.AddButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
#if QT_CONFIG(tooltip)
        self.DeleteButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Press to Delete</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.DeleteButton.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
#if QT_CONFIG(tooltip)
        self.BrowseButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Press to Browse</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.BrowseButton.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.ShowButton.setText(QCoreApplication.translate("MainWindow", u"Show", None))
        self.HideButton.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
    # retranslateUi

