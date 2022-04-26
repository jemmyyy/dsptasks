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
import pyqtgraph as pg
from os import path, remove 
from numpy.polynomial import Polynomial as P
from logging import error
import math
from math import ceil, inf
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from numpy.core.fromnumeric import size
import pandas as pd
from pyqtgraph.widgets.PlotWidget import PlotWidget
import pyqtgraph as pg
from scipy import interpolate
from scipy import signal
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from scipy.fftpack.basic import fft
import seaborn as sns
import matplotlib.pyplot as plt
import sys


FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"task4.ui"))

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        fig.tight_layout()

class MyThread(QThread):
    change_value = pyqtSignal(int)
    def run(self):
        cnt = 0
        while cnt < 100:
            cnt+=1
            self.change_value.emit(cnt)

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
      
        self.chunkSlider.setMinimum(1)
        self.chunkSlider.setMaximum(25)
        self.chunkSlider.setValue(0)
        self.chunkSlider.setTickInterval(1)
        self.chunkSlider.setSingleStep(1)
        self.chunkSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.chunkSlider.valueChanged.connect( self.chunkChange)


        self.orderSlider.setMinimum(1)
        self.orderSlider.setMaximum(25)
        self.orderSlider.setValue(0)
        self.orderSlider.setTickInterval(1)
        self.orderSlider.setSingleStep(1)
        self.orderSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.orderSlider.valueChanged.connect(self.orderChange)

        self.splitter_AllGraphs = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_AllGraphs.setGeometry(QtCore.QRect(40, 80, 1000, 300)) 
        self.splitter_AllGraphs.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_AllGraphs.setObjectName("splitter_AllGraphs")
        self.graphicsView_main = PlotWidget(self.splitter_AllGraphs)
        self.graphicsView_main.setStyleSheet("background: rgb(255,255,255)")
        self.graphicsView_main.setObjectName("graphicsView_main")
        self.graphicsView_main.setTitle("Main Graph")
        self.splitter_AllGraphs.addWidget(self.graphicsView_main)
        self.blue_pen= pg.mkPen((0,0,255), width=2, style=QtCore.Qt.DotLine)
        self.intial_slider_order_val=1;
        self.chunk_size = 1000
        self.extrapolation_pecentage = 100

        # self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 80, 811, 300))
        # self.splitter_graphs = QtWidgets.QSplitter(self.centralwidget)
        # self.splitter_graphs.setGeometry(QtCore.QRect(110, 100, 100, 331))
        # self.splitter_graphs.setOrientation(QtCore.Qt.Horizontal)
        # self.splitter_graphs.setObjectName("splitter_graphs")
        # self.gridLayout.addWidget(self.splitter_graphs,0,1,6,4)
        
        # self.canvas = MplCanvas(self, width=10, height=4, dpi=100)
        # self.splitter_graphs.addWidget(self.canvas)
        # self.intial_slider_order_val = 1
    def Handle_Buttons(self):
         self.BrowseButton.clicked.connect(self.Browse)

    def Browse(self):
        self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open csv', QtCore.QDir.rootPath(), 'csv(*.csv)')
        self.data_set = pd.read_csv(self.fileName, header=None)
        self.data_amplitude = self.data_set[1]
        self.x_axis_data = self.data_set[0]
        # self.canvas.draw()
        self.Get_max_freq()
        self.plotting_data(self.intial_slider_order_val)


    def Get_max_freq(self):
        data_amp=[]
        n=size(self.data_amplitude)

        for i in self.data_amplitude:
            if len(data_amp)== len(self.x_axis_data):
                break
            else:
                data_amp.append(i)

        frequencies_array=np.arange(1,n/2,dtype ='int')
        data_freq=fft(data_amp)
        freq_mag=(2/n)*abs(data_freq[0:np.size(frequencies_array)])

        imp_freq=freq_mag>0.2
        clean_frequencies_array=imp_freq*frequencies_array
        self.fmax=round(clean_frequencies_array.max())

    def plotting_data(self,order_val):
        if self.fmax == 0:
            self.graphicsView_main.clear()
            self.graphicsView_main.plot(self.x_axis_data,self.data_amplitude)
        else:
            self.graphicsView_main.clear()
            self.graphicsView_main.plotItem.vb.setLimits(xMin=min(self.x_axis_data)-0.01, xMax=max(self.x_axis_data),yMin=min(self.data_amplitude) - 0.2, yMax=max(self.data_amplitude) + 0.2)
            self.graphicsView_main.plot(self.x_axis_data,self.data_amplitude)
            self.interpolate_the_curve(order_val)

    def interpolate_the_curve(self,interpol_order):
        self.chunk_coeffs = []
        self.residuals = []
        for i in range(0,len(self.x_axis_data)-1,self.chunk_size):
            data = []
            t = []
            ind = i
            for j in range(self.chunk_size-1):
                if ind < len(self.x_axis_data):
                    data.append(self.data_amplitude[ind])
                    t.append(self.x_axis_data[ind])
                    ind += 1
            extrapolation_fraction = self.extrapolation_pecentage/100
            interpol_range = int(extrapolation_fraction*(self.chunk_size-1))
            self.coeffs,res, _, _, _= np.polyfit(t[0:interpol_range], data[0:interpol_range], interpol_order, full=True)
            if res.size != 0:
                self.residuals.append(res[0])
            self.chunk_coeffs.append(self.coeffs)

            p = np.poly1d(self.coeffs)
            self.graphicsView_main.plot(t,p(t),pen = self.blue_pen)

    def interpolate(self,interpol_order,chunk):
        sampling_rate=int(2.5*self.fmax)
        sample_time = 1/sampling_rate
        no_of_samples = int(max(self.x_axis_data)/sample_time)
        for i in range(0,len(self.x_axis_data)-1,chunk):
            data = []
            t = []
            ind = i
            for j in range(chunk-1):
                if ind < len(self.x_axis_data):
                    data.append(self.data_amplitude[ind])
                    t.append(self.x_axis_data[ind])
                    ind += 1
            self.Sample_amp,self.Sample_time = signal.resample(data,no_of_samples,t)
            z = np.polyfit(self.Sample_time, self.Sample_amp, interpol_order)
            p = np.poly1d(z)
            y = p(t)
            return p 

    def orderChange(self):
        self.intial_slider_order_val = int(self.orderSlider.value())
        self.plotting_data(self.intial_slider_order_val)
        self.latex_eqn(self.intial_slider_order_val)

    def chunkChange(self):
        self.comboBox.clear()
        self.slider_chunk_val = self.chunkSlider.value()
        self.chunk_size = ceil(1000 / self.slider_chunk_val)
        self.plotting_data(self.intial_slider_order_val)
        for i in range(self.slider_chunk_val):
            self.comboBox.addItem(str(self.slider_chunk_val - i))


        
def main ():
    app = QApplication(sys.argv)
    window = MainApp ()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()