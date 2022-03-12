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
from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Codemy.com - Learn To Code!')

FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"main.ui"))

class MainApp(QMainWindow , FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI()
        

        self.counter = 0
        self.max_len = 0
        self.Signal_Flag = 1
        self.First_Signal_Flag = 0
        self.Second_Signal_Flag = 0
        self.Third_Signal_Flag = 0
        
        self.isRunning=True

        self.Hide_First_Signal_Flag = 0
        self.Hide_Second_Signal_Flag = 0
        self.Hide_Third_Signal_Flag = 0

        self.pen1 = pg.mkPen('r')
        self.pen2 = pg.mkPen('b')
        self.pen3 = pg.mkPen('y')

    def Handel_UI(self):
        # self = QMainWindow
        self.setWindowTitle('Multi-Channel Signal Viewer')
        self.Handel_Buttons()
        self.Handel_GraphicsViews()
        # self.Handel_Slider()

    def Handel_Buttons(self):
        self.BrowseButton_13.clicked.connect(self.Handel_Browse)
        self.ShowcomboBox.currentTextChanged.connect(self.Handel_Show)
        self.HidecomboBox.currentTextChanged.connect(self.Handel_Hide)
        self.horizontalSlider_2.setMinimum(-1000)
        self.horizontalSlider_2.setMaximum(1000)
        self.horizontalSlider_2.setValue(0)
        self.horizontalSlider_2.setTickPosition(QSlider.TicksBelow)
        self.horizontalSlider_2.setTickInterval(100)
        # self.horizontalSlider_2.valueChanged.connect(self.Handel_Slider)
        self.PauseButton_6.clicked.connect(self.Handel_pause)
        self.PlayButton_7.clicked.connect(self.Handel_play)
        # Zoom Button Functions
        self.zoomInButton.clicked.connect(self.zoomIn)
        self.zoomOutButton.clicked.connect(self.zoomOut)
        # Scroll Slider Functions
        self.horizontalScroll.valueChanged.connect(self.scrollHorizontal)
        self.horizontalScroll.sliderMoved.connect(self.scrollHorizontal)
        self.horizontalScroll.sliderReleased.connect(self.scrollHorizontal)
        self.verticalScroll.valueChanged.connect(self.scrollVertical)
        self.verticalScroll.sliderMoved.connect(self.scrollVertical)
        self.verticalScroll.sliderReleased.connect(self.scrollVertical)


    # def Handel_Slider(self):
    #       self.speed=self.speed+self.horizontalSlider_2.value()
    #       if(self.speed > 0):
    #          self.timer.setInterval(self.speed)
    #          self.timer.timeout.connect(self.update_plot_data)
    #          self.timer.start()

    def Handel_GraphicsViews(self):
         pass

    def Handel_pause(self):
            self.isRunning=False        
    
    def Handel_play(self):
            self.isRunning=True   

    def zoomIn(self):
        self.Handel_pause
        self.graphicsView.plotItem.getViewBox().scaleBy((0.85,0.85))

    def zoomOut(self):
        self.Handel_pause
        self.graphicsView.plotItem.getViewBox().scaleBy((1.15,1.15))

    def scrollHorizontal(self):
            self.horizontalScroll.setMaximum(self.max_len)
            self.horizontalScroll.setMinimum(0)
            val = self.horizontalScroll.value()
            self.graphicsView.setXRange(val-50, val+50)

    def scrollVertical(self):
            self.verticalScroll.setMaximum(self.maxAmp)
            self.verticalScroll.setMinimum(self.minAmp)
            val = self.verticalScroll.value()
            self.graphicsView.setYRange(val-((self.maxAmp-self.minAmp) / 5), val+((self.maxAmp-self.minAmp) / 5))


    def Handel_Show(self) :
        item = self.HidecomboBox.currentText()
        if item == "Signal_1" :
            self.Hide_First_Signal_Flag = 0
            self.Signal1 = self.graphicsView.plot(self.x1[0:self.counter],self.y1[0:self.counter], pen=self.pen1)
        elif item == "Signal_2" :
            self.Hide_Second_Signal_Flag = 0
            self.Signal2 = self.graphicsView.plot(self.x2[0:self.counter],self.y2[0:self.counter], pen=self.pen1)
        elif item == "Signal_3" :
            self.Hide_Third_Signal_Flag = 0
            self.Signal3 = self.graphicsView.plot(self.x3[0:self.counter],self.y3[0:self.counter], pen=self.pen1)
        else :
            self.Hide_First_Signal_Flag = 0
            self.Signal1 = self.graphicsView.plot(self.x1[0:self.counter],self.y1[0:self.counter], pen=self.pen1)
            self.Hide_Second_Signal_Flag = 0
            self.Signal2 = self.graphicsView.plot(self.x2[0:self.counter],self.y2[0:self.counter], pen=self.pen1)
            self.Hide_Third_Signal_Flag = 0
            self.Signal3 = self.graphicsView.plot(self.x3[0:self.counter],self.y3[0:self.counter], pen=self.pen1)


    def Handel_Hide(self):
        item = self.HidecomboBox.currentText()
        if item == "Signal_1" :
            self.Hide_First_Signal_Flag = 1
            self.Signal1.hide()
        elif item == "Signal_2" :
            self.Hide_Second_Signal_Flag = 1
            self.Signal2.hide()
        elif item == "Signal_3" :
            self.Hide_Third_Signal_Flag = 1
            self.Signal3.hide()
        else :
            self.Hide_First_Signal_Flag = 1
            self.Signal1.hide()
            self.Hide_Second_Signal_Flag = 1
            self.Signal2.hide()
            self.Hide_Third_Signal_Flag = 1
            self.Signal3.hide()

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
            self.x1 = np.array(self.time)
            self.y1 = np.array(self.amplitude)
            self.maxAmp = max(self.y1)
            self.minAmp = min(self.y1)
            if (self.maxAmp - self.minAmp) < 5:
                self.y1*=10
                self.maxAmp = max(self.y1)
                self.minAmp = min(self.y1)
            self.Signal_Flag = 2
            self.First_Signal_Flag = 1
        elif self.Signal_Flag == 2:
            self.x2 = np.array(self.time)
            self.y2 = np.array(self.amplitude)
            if (max(self.y2) - min(self.y2)) < 5:
                self.y2*=10
            if max(self.y2) > self.maxAmp:
                self.maxAmp = max(self.y2)
            if min(self.y2) < self.minAmp:
                self.minAmp = min(self.y2)
            self.Second_Signal_Flag = 1
            self.Signal_Flag = 3
        elif self.Signal_Flag == 3:
            self.x3 = np.array(self.time)
            self.y3 = np.array(self.amplitude)
            if (max(self.y3) - min(self.y3)) < 5:
                self.y3*=10
            if max(self.y3) > self.maxAmp:
                self.maxAmp = max(self.y3)
            if min(self.y3) < self.minAmp:
                self.minAmp = min(self.y3)
            self.Signal_Flag = 1
            self.Third_Signal_Flag = 1
        self.timer()
    def timer(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)                       #In control of speed :)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
    def update_plot_data(self):
        start_count = 0
        end_count = 0
        if self.isRunning :
            self.counter = self.counter +10
            
        self.graphicsView.clear()
        if self.First_Signal_Flag == 1 and self.Hide_First_Signal_Flag == 0:
            self.Signal1 = self.graphicsView.plotItem.plot(self.x1[0:self.counter],self.y1[0:self.counter], pen=self.pen1)               #Plot every 100 x index with 100 y index
            self.max_len = len(self.x1)
        if self.Second_Signal_Flag == 1 and self.Hide_Second_Signal_Flag == 0:
            self.Signal2 = self.graphicsView.plot(self.x2[0:self.counter],self.y2[0:self.counter], pen=self.pen2)
            self.max_len = max(len(self.x1),len(self.x2))
        if self.Third_Signal_Flag == 1 and self.Hide_Third_Signal_Flag == 0:
            self.Signal3 = self.graphicsView.plot(self.x3[0:self.counter],self.y3[0:self.counter], pen=self.pen3)
            self.max_len = max(len(self.x1),len(self.x2),len(self.x3))
        
        if self.counter < self.max_len:                                                    #To stop at the limit of the graph
            if self.counter < 100:
                start_count = 0
                end_count = 100
            else:
                start_count = self.counter - 100
                end_count = self.counter
                self.graphicsView.setXRange(start_count,end_count)
                self.graphicsView.setYRange(self.minAmp, self.maxAmp)
def main ():
    app = QApplication(sys.argv)
    window = MainApp ()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main()