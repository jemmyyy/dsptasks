##PyQT5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from pyqtgraph import PlotWidget,plot
from PyQt5 import QtCore
import sys
import os 
import pyqtgraph as pg
from os import path 
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import signal 

FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"main.ui"))

class MainApp(QMainWindow , FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI()
        self.counter = 0
        self.speed=2000
        self.isRunning=True
        self.max_len = 0
        self.pen = pg.mkPen('r')

    def Handle_UI(self):
        self.setWindowTitle('Sampling-Theory Illustrator')
        self.Handle_Buttons()

    def Handle_Buttons(self):
         self.BrowseButton.clicked.connect(self.Browse)
         self.ShowButton.clicked.connect(self.Show_Signal_Composer)
         self.AddButton.clicked.connect(self.Add)
         self.ConfirmButton.clicked.connect(self.Confirm)
         self.SaveButton.clicked.connect(self.Save)

    def Add (self): 
        pass

    def Save (self): 
        pass

    def Confirm (self): 
        pass


    def Browse(self):
        open_place = QFileDialog.getOpenFileName(self , caption= "Browse", directory=".", filter="All Files (*.*)")
        path = open_place[0].split(',') #path refears to the chosen file after splitting  
        myfile = open(path[0], "r") # 'r' refears to the mode, the mode here is reading 
        self.Amplitude = []
        self.Time = []
        self.sigDatax=[]
        self.sigDatay=[]
        while myfile:
            myline  = myfile.readline()
            if myline == "": 
                 break
            self.line = myline.split() 
            self.Amplitude.append(float(self.line [0]))
            self.Time.append(float(self.line [1])) 
        myfile.close()
        self.x = np.array(self.Time)
        self.y = np.array(self.Amplitude)
        self.update_plot_data()
    
    def Plot(self):
        self.Signal = self.PlotgraphicsView.plot(self.x,self.y, pen='#FFFF00')
        self.PlotgraphicsView.setLimits(xMin = 0, xMax = self.x[101])

    def Show_Signal_Composer(self):
        self.ComposergraphicsView.clear()
        self.Amplitude = float(self.Amplitude_textEdit.toPlainText())
        self.Frequency = float(self.Frequency_textEdit.toPlainText())
        self.Phase_Shift = float(self.Phase_Shift_textEdit.toPlainText())
        current_comboBox_item = self.SignalcomboBox.currentText()
        if current_comboBox_item == "Sine Signal" :
          signal = self.Amplitude * np.sin(2* np.pi * self.Frequency * self.Time + self.Phase_Shift)
        elif current_comboBox_item == "Cosine Signal" :
          signal = self.Amplitude * np.cos(2* np.pi * self.Frequency * self.Time + self.Phase_Shift)
        
          

def main ():
    app = QApplication(sys.argv)
    window = MainApp ()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()