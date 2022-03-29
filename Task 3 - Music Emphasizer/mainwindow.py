##PyQT5
from fileinput import filename
import string
from subprocess import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget,plot
from PyQt5 import QtCore
import os 
import csv 
import pyqtgraph as pg
from os import path, remove 
import numpy as np
import pandas as pd
import math  
import matplotlib.pyplot as plt
import scipy
from scipy.fftpack import fft
from scipy import signal 
from tkinter import filedialog
from tkinter import *
import sys


FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"qtFiles/main.ui"))

new_sig=[]
t = np.arange(0, 1, 0.001)

class MainApp(QMainWindow , FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI()

    def Handle_UI(self):
        self.setWindowTitle('Sampling-Theory Illustrator')
        self.Handle_Buttons()

    def Handle_Buttons(self):
        self.Instrument1verticalSlider.setMaximum(8)
        self.Instrument1verticalSlider.setMinimum(0)
        self.Instrument1verticalSlider.setValue(4)
        self.Instrument2verticalSlider.setMaximum(8)
        self.Instrument2verticalSlider.setMinimum(0)
        self.Instrument2verticalSlider.setValue(4)
        self.Instrument3verticalSlider.setMaximum(8)
        self.Instrument3verticalSlider.setMinimum(0)
        self.Instrument3verticalSlider.setValue(4)

    def Handle_Buttons(self):
        self.Instrument1verticalSlider.setMaximum(8)


        
def main ():
    app = QApplication(sys.argv)
    window = MainApp ()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
