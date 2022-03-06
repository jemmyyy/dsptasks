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

FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"main.ui"))

class MainApp(QMainWindow , FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI()
        self.counter = 0
        self.pen = pg.mkPen('r')
    def Handel_UI(self):
        ## self = QMainWindow
        self.setWindowTitle('Multi-Channel Signal Viewer')
        self.Handel_Buttons()
        self.Handel_GraphicsViews()
        self.Handel_Slider()
    def Handel_Buttons(self):
        self.BrowseButton_13.clicked.connect(self.Handel_Browse)
        self.ShowButton_4.clicked.connect(self.Handel_Show)
        self.HideButton_5.clicked.connect(self.Handel_Hide)
        self.ZoomInButton.clicked.connect(self.Handel_ZoomIn)
    def Handel_Slider(self):
         pass

    def Handel_GraphicsViews(self):
         pass

    def Handel_Show(self):
          self.pen = pg.mkPen('r')

    def Handel_ZoomIn(self):
        pass

    def Handel_Hide(self):
          self.pen = pg.mkPen('k')

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
         self.x = np.array(self.time)
         self.y = np.array(self.amplitude)
         self.timer()

    def timer(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(200)                       #In control of speed :)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        
    
    def update_plot_data(self):
        self.graphicsView.plot(self.x[0:self.counter],self.y[0:self.counter], pen=self.pen)
        self.counter = self.counter + 100
        self.graphicsView.clear()

        self.graphicsView.plot(self.x[0:self.counter],self.y[0:self.counter], pen=self.pen)               #Plot every 100 x index with 100 y index
        if self.counter < len(self.x):                                                        #To stop at the limit of the graph
            self.graphicsView.setXRange( self.counter-200,self.counter)

def main ():
    app = QApplication(sys.argv)
    window = MainApp ()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()