##PyQT5
from distutils import extension
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import  loadUiType
from pyqtgraph import PlotWidget,plot
from PyQt5 import QtCore
import numpy as np
import pyqtgraph as pg
import sys
import os 
from os import path

# from sympy import false, true 

FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"main.ui"))

class MainApp(QMainWindow , FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI()
        
        self.speed=2000
        self.zoom = 1
        self.counter = 0
        self.isRunning=True
        self.Signal_Flag = 1   
        self.First_Signal_Flag = 0
        self.Second_Signal_Flag = 0
        self.Third_Signal_Flag = 0

        self.pen1 = pg.mkPen('r')
        self.pen2 = pg.mkPen('b')
        self.pen3 = pg.mkPen('y')

    def Handel_UI(self):
        ## self = QMainWindow
        self.setWindowTitle('Multi-Channel Signal Viewer')
        self.Handel_Buttons()
        self.Handel_GraphicsViews()
    def Handel_Buttons(self):
        self.horizontalSlider_2.setMinimum(-1000)
        self.horizontalSlider_2.setMaximum(1000)
        self.horizontalSlider_2.setValue(0)
        self.horizontalSlider_2.setTickPosition(QSlider.TicksBelow)
        self.horizontalSlider_2.setTickInterval(100)
        self.horizontalSlider_2.valueChanged.connect(self.Handel_Slider)
        self.BrowseButton_13.clicked.connect(self.Handel_Browse)
        self.ShowButton_4.clicked.connect(self.Handel_Show)
        self.HideButton_5.clicked.connect(self.Handel_Hide)
        self.PauseButton_6.clicked.connect(self.Handel_pause)
        self.PlayButton_7.clicked.connect(self.Handel_play)
        self.Zoom_InButton_2.clicked.connect(self.Handel_ZoomIn)
        self.Zoom_OutButton_3.clicked.connect(self.Handel_ZoomOut)
        
        
    def Handel_Slider(self):
         self.speed=self.speed+self.horizontalSlider_2.value()
         if(self.speed > 0):
            self.timer.setInterval(self.speed)
            self.timer.timeout.connect(self.update_plot_data)
            self.timer.start()

    def Handel_GraphicsViews(self):
         pass

    def Handel_ZoomIn(self):
        self.graphicsView.scale(2,2)
    def Handel_ZoomOut(self):
        self.graphicsView.scale(0.5,0.5)

    def Handel_Show(self):
          self.pen = pg.mkPen('r')

    def Handel_Hide(self):
          self.pen = pg.mkPen('k')
    
    def Handel_pause(self):
            self.isRunning=False        
    
    def Handel_play(self):
            self.isRunning=True        

    def Handel_Browse(self):
        open_place = QFileDialog.getOpenFileName(self , caption= "Browse", directory=".", filter="All Files (*.*)")
        path = open_place[0].split(',') 
        myfile = open(path[0], "r") #path refears to the chosen file after splitting   # 'r' refears to the mode, the mode here is reading 
        self.amplitude = []
        self.time = []
        while myfile:
            myline  = myfile.readline()
            if myline == "":  break
            line = myline.split() 
            self.amplitude.append(float(line [0]))
            self.time.append(float(line [1])) 
        myfile.close()
        if self.Signal_Flag == 1:
            self.x = np.array(self.time)
            self.y = np.array(self.amplitude)
            self.Signal_Flag = 2
            self.First_Signal_Flag = 1

        elif self.Signal_Flag == 2:
            self.x2 = np.array(self.time)
            self.y2 = np.array(self.amplitude)
            self.Second_Signal_Flag = 1
            self.Signal_Flag = 3

        elif self.Signal_Flag == 3:
            self.x3 = np.array(self.time)
            self.y3 = np.array(self.amplitude)
            self.Signal_Flag = 1
            self.Third_Signal_Flag = 1

        self.timer()

    def timer(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.speed)                       #In control of speed 
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        
    
    def update_plot_data(self):
        start_count = 0
        end_count = 0
        if self.isRunning :
            self.counter = self.counter +    10
        self.graphicsView.clear()

        if self.First_Signal_Flag == 1:
            self.graphicsView.plot(self.x[0:self.counter],self.y[0:self.counter], pen=self.pen1)               #Plot every 100 x index with 100 y index
        
        if self.Second_Signal_Flag == 1:
            self.graphicsView.plot(self.x2[0:self.counter],self.y2[0:self.counter], pen=self.pen2)
        
        if self.Third_Signal_Flag == 1:
            self.graphicsView.plot(self.x3[0:self.counter],self.y3[0:self.counter], pen=self.pen3)
        
        if self.counter < len(self.x):                                                    #To stop at the limit of the graph
            if self.counter < 100:
                start_count = 0
                end_count = 100
            else:
                start_count = self.counter - 100
                end_count = self.counter

            self.graphicsView.setXRange(start_count,end_count)

def main ():
    app = QApplication(sys.argv)
    window = MainApp ()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()