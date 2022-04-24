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


FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"qtFiles/task4.ui"))

new_sig=[]
t = np.arange(0, 1, 0.001)

class MainApp(QMainWindow , FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI()
        self.fmax = -1000

    def Handle_UI(self):
        self.setWindowTitle('Interpolation and Curve Fitting')
        self.Handle_Buttons()

    def Handle_Buttons(self):
         self.BrowseButton.clicked.connect(self.Browse)

    def GetMaxFreq(self, Amplitude, time):
        data_amp=[]
        for i in Amplitude:
            if len(data_amp)== len(t):
                break
            else:
                data_amp.append(i)

        timeLength=np.size(time)
        frequencies_array=np.arange(1, np.floor(timeLength/2), 10, dtype ='int')
        print(len(frequencies_array))
        data_freq=fft(data_amp)

        freq_mag=(2/timeLength)*abs(data_freq[0:np.size(frequencies_array)])

        imp_freq=freq_mag>0.2
        clean_frequencies_array=imp_freq*frequencies_array
        self.fmax=round(clean_frequencies_array.max())
        print(clean_frequencies_array)


    def Browse(self):
        self.PlotgraphicsView.clear()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open csv', QtCore.QDir.rootPath(), 'csv(*.csv)')
        dataSet = pd.read_csv(fileName, header=None)
        self.amplitudeData = dataSet[1]
        self.timeData = dataSet[0]
        if self.amplitudeData[20001]:
            self.fmax = self.amplitudeData[20001]
            self.amplitudeData = self.amplitudeData[0:20000]
            self.timeData = self.timeData[0:20000]
        else:
            self.GetMaxFreq(self.amplitudeData, self.timeData)
        self.plotMainGraph(self.amplitudeData, self.timeData, 0)

        
def main ():
    app = QApplication(sys.argv)
    window = MainApp ()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()