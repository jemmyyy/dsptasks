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
        self.SignalsCounter = 1
        self.added_signal = 0 
        self.counter_signal = 0
        self.list_signal = [] 
        self.y = 0
        self.fmax = -1000
        self.counter = 0
        self.max_len = 0
        self.pen = pg.mkPen('r')
        self.orange_pen = pg.mkPen((255,215,0) , width=1)

    def Handle_UI(self):
        self.setWindowTitle('Sampling-Theory Illustrator')
        self.Handle_Buttons()
        #self.Handle_GraphicsViews()
        self.horizontalSlider.setMaximum(12)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setTickPosition(QSlider.TicksBelow)

    def Handle_Buttons(self):
         self.BrowseButton.clicked.connect(self.Browse)
         self.ApplyButton.clicked.connect(self.Show_Signal_Composer)
         self.AddButton.clicked.connect(self.Add)
         self.DeleteButton.clicked.connect(self.Delete)
         self.ConfirmButton.clicked.connect(self.Confirm)
         self.ShowButton.clicked.connect(self.Show)
         self.HideButton.clicked.connect(self.Hide)
         self.SaveButton.clicked.connect(self.Save_Signal)
         self.horizontalSlider.valueChanged.connect(self.Sampling_change)

    def Hide (self):
        self.ComposergraphicsView.hide()
        self.graphicsView_3.hide()
        self.reconstructGraphicsView.hide()
    def Show (self):  
        self.ComposergraphicsView.show()
        self.graphicsView_3.show()
        self.reconstructGraphicsView.show()

    def Add (self): 
        self.graphicsView_3.clear()
        self.list_signal.append(self.signal)
        self.added_signal = self.added_signal + self.signal
        self.graphicsView_3.plot(self.t , self.added_signal, pen = self.pen)
        self.graphicsView_3.plotItem.vb.setLimits(xMin = min(self.t), xMax = max(self.t), yMin = min(self.added_signal), yMax = max(self.added_signal))

        self.text = 'A:' +str(self.Amplitude) + '_F:' +str(self.Frequency)+ '_P:' +str(self.Phase_Shift)
        self.DeletecomboBox.addItem(self.text)
        self.counter_signal +=1
    
    def Delete(self):
         delete_item_index = self.DeletecomboBox.currentIndex()
         removed_signal = self.list_signal[delete_item_index]
         self.list_signal.pop(delete_item_index)
         self.DeletecomboBox.removeItem(delete_item_index)
         self.added_signal = self.added_signal - removed_signal 
         self.graphicsView_3.clear()
         if self.DeletecomboBox.count() > 0 :
            self.graphicsView_3.plot(self.t , self.added_signal, pen = self.pen)
            self.graphicsView_3.plotItem.vb.setLimits(xMin = min(self.t), xMax = max(self.t), yMin = min(self.added_signal), yMax = max(self.added_signal))


    def Save_Signal (self): 
        print(self.fmax)
        self.t = np.append(self.t, self.fmax)
        self.added_signal = np.append(self.added_signal, self.fmax)
        SavedSignal = np.column_stack((self.t,self.added_signal))
        Save_Text = self.Save_textEdit.toPlainText()
        with open(Save_Text+'.csv', 'w') as f:
           write = csv.writer(f)
           
           write.writerows(SavedSignal)
                
    def Confirm (self): 
        self.y = self.y + self.added_signal
        
        self.timeData = self.t
        self.amplitudeData = self.y
        self.plotGraphicsView.clear()
        self.plotGraphicsView.plot(self.t, self.y)
        self.plotGraphicsView.plotItem.vb.setLimits(xMin = min(self.t), xMax = max(self.t), yMin = min(self.y), yMax = max(self.y))
    
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
        self.ComposergraphicsView.clear()
        self.reconstructGraphicsView.clear() 
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

    def plotMainGraph(self, amplitude,time,Fs):
        self.plotGraphicsView.plotItem.vb.setLimits(xMin=min(time)-0.01, xMax=max(time),yMin=min(amplitude) - 0.2, yMax=max(amplitude) + 0.2)
        if Fs == 0:
            self.plotGraphicsView.clear()
            self.plotGraphicsView.plot(time,amplitude)
        else:
            sample_time = 1/Fs
            no_of_samples = math.ceil(max(time))/sample_time
            no_of_samples = math.ceil(no_of_samples)
            index_append= len(time)/no_of_samples
            index_append = math.floor(index_append)
            self.Sample_amp=[]
            self.Sample_time = []
            index = 0

            for i in range(no_of_samples):
                self.Sample_time.append(time[index])
                self.Sample_amp.append(amplitude[index])
                index += index_append

            self.recons_amp = self.sinInterpolate(self.Sample_amp,self.Sample_time,time)

            self.plotGraphicsView.clear()
            self.reconstructGraphicsView.clear()
            self.plotGraphicsView.plot(time, amplitude)
            self.plotGraphicsView.plot(self.Sample_time, self.Sample_amp, symbol='o', pen = None)
            self.plotGraphicsView.plot(time, self.recons_amp, pen = self.orange_pen)
            self.reconstructGraphicsView.plot(time, self.recons_amp, pen=self.orange_pen)
            self.reconstructGraphicsView.plotItem.vb.setLimits(xMin=min(self.timeData) - 0.01,xMax=max(self.timeData),yMin=min(self.amplitudeData) - 0.2,yMax=max(self.amplitudeData) + 0.2)
    
    def sinInterpolate(self, sample_amplitude, sample_time, time):
         if len(sample_amplitude) != len(sample_time):
             raise ValueError('sample time and sample amplitude must be the same length')

         sample_time = np.array(sample_time)
         time = np.array(time)

         # Find the period
         period_time = sample_time[1] - sample_time[0]

         sincM = np.tile(time, (len(sample_time), 1)) - np.tile(sample_time[:, np.newaxis], (1, len(time)))
         recovered_signal = np.dot(sample_amplitude, np.sinc(sincM / period_time))
         return recovered_signal


    def Sampling_change(self):
        value = float(self.horizontalSlider.value())
        if (value/4)*self.fmax*max(self.timeData) <3:
            value = 3/(max(self.timeData*self.fmax))
        else:
            value = value / 4

        self.plotMainGraph(self.amplitudeData,self.timeData,self.fmax*value)
 

    def Show_Signal_Composer(self):
        self.ComposergraphicsView.clear()
        self.Amplitude = float(self.Amplitude_textEdit.toPlainText())
        self.Frequency = float(self.Frequency_textEdit.toPlainText())
        if self.Frequency > self.fmax:
            self.fmax = self.Frequency
        self.Phase_Shift = float(self.Phase_Shift_textEdit.toPlainText())
        self.Phase_Shift =  self.Phase_Shift*np.pi/180
        self.t = np.arange(0,20,1/1000)
        current_comboBox_item = self.SignalcomboBox.currentText()
        if current_comboBox_item == "Sine Signal" :
          self.signal = self.Amplitude * np.sin(2* np.pi * self.Frequency * self.t + self.Phase_Shift)
        elif current_comboBox_item == "Cosine Signal" :
          self.signal = self.Amplitude * np.cos(2* np.pi * self.Frequency * self.t + self.Phase_Shift)
        self.ComposergraphicsView.plot(self.t , self.signal, pen = self.pen)
        self.ComposergraphicsView.plotItem.vb.setLimits(xMin = min(self.t), xMax = max(self.t), yMin = min(self.signal), yMax = max(self.signal))

        
def main ():
    app = QApplication(sys.argv)
    window = MainApp ()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
