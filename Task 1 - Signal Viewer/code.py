##PyQT5
from distutils import extension
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import  loadUiType

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
    def Handel_UI(self):
        ## self = QMainWindow
        self.setWindowTitle('Multi-Channel Signal Viewer')
        self.Handel_Buttons()
        self.Handel_GraphicsViews()
        self.Handel_Slider()
    def Handel_Buttons(self):
        self.BrowseButton_13.clicked.connect(self.Handel_Browse)

    def Handel_Slider(self):
         pass

    def Handel_GraphicsViews(self):
         pass

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

def main ():
    app = QApplication(sys.argv)
    window = MainApp ()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()