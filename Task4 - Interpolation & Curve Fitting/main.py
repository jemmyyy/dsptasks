##PyQT5
from ast import Return
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
from scipy.interpolate import  CubicSpline, make_interp_spline

############
# from PyQt4 import QtCore, QtGui  
# from final_ar_gui import *

from PyQt5.QtWidgets import QApplication, QDialog, QProgressBar, QPushButton
from PyQt5.QtCore import Qt, QThread, pyqtSignal

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
        self.extrapolation_sliderval = 1
        self.extrapolation_pecentage = 100

    def Handle_UI(self):
        self.setWindowTitle('Interpolation and Curve Fitting')
        self.Handle_Buttons()
      
        self.chunkSlider.setMinimum(1)
        self.chunkSlider.setMaximum(15)
        self.chunkSlider.setValue(0)
        self.chunkSlider.setTickInterval(1)
        self.chunkSlider.setSingleStep(1)
        self.chunkSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.chunkSlider.valueChanged.connect(self.chunkChange)
        self.chunkSlider.valueChanged.connect(lambda: self.Latex_Equation( int(self.orderSlider.value())))
        
        self.orderSlider.setMinimum(1)
        self.orderSlider.setMaximum(15)
        self.orderSlider.setValue(0)
        self.orderSlider.setTickInterval(1)
        self.orderSlider.setSingleStep(1)
        self.orderSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.orderSlider.valueChanged.connect(self.orderChange)
        self.orderSlider.valueChanged.connect(lambda: self.Latex_Equation( int(self.orderSlider.value())))

        self.extrapolationSlider.setMinimum(1)
        self.extrapolationSlider.setMaximum(5)
        self.extrapolationSlider.setValue(0)
        self.extrapolationSlider.setTickInterval(1)
        self.extrapolationSlider.setSingleStep(1)
        self.extrapolationSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.extrapolationSlider.valueChanged.connect(lambda: self.extrapolation_change())

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

        self.frame_graph = QtWidgets.QFrame(self.centralwidget)
        self.frame_graph.setGeometry(QtCore.QRect(160, 35, 570, 40))
        self.frame_graph.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_graph.setFrameShadow(QtWidgets.QFrame.Raised)
        self.LAYOUT_Graph = QtWidgets.QGridLayout()
        self.frame_graph.setLayout(self.LAYOUT_Graph)
        self.fig = Figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.LAYOUT_Graph.addWidget(self.canvas, *(0, 1))
        self.fig.clear()

        self.fig_error = Figure()
        self.frame_error = QtWidgets.QFrame(self.centralwidget)
        self.frame_error.setGeometry(QtCore.QRect(850, 35, 230, 40))
        self.frame_error.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_error.setFrameShadow(QtWidgets.QFrame.Raised)
        self.LAYOUT_Error = QtWidgets.QGridLayout()
        self.frame_error.setLayout(self.LAYOUT_Error)
        self.canvas_error = FigureCanvasQTAgg(self.fig_error)
        self.LAYOUT_Error.addWidget(self.canvas_error, *(0, 1))
        self.fig_error.clear()
        self.hidden=False

        self.comboBox_2.addItem("Order of polynomial")
        self.comboBox_2.addItem("no. of chunks")
        self.comboBox_2.addItem("Over lapping")
        # self.comboBox_3.addItem("Order of polynomial")
        self.comboBox_3.addItem("no. of chunks")
        self.comboBox_3.addItem("Over lapping")
        self.comboBox.currentTextChanged.connect(self.latexeqn)
        # self.NumberofChunks.setValue(5)
        # self.PolynomialOrder.setValue(5)
        self.bool_heatmap = 0

    def Handle_Buttons(self):
         self.BrowseButton.clicked.connect(self.Browse)
         self.pushButton.clicked.connect(self.error_map)
         self.comboBox_2.activated.connect(self.conection)
        #  self.comboBox_3.activated.connect(self.conection2)
         self.interpolationSelector.activated.connect(self.interpolation_method)

    def Browse(self):
        self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open csv', QtCore.QDir.rootPath(), 'csv(*.csv)')
        self.data_set = pd.read_csv(self.fileName, header=None)
        self.data_amplitude = self.data_set[1]
        self.x_axis_data = self.data_set[0]
        self.plot_data(self.intial_slider_order_val)


    def plot_data(self,order_val):
            self.graphicsView_main.clear()
            self.graphicsView_main.plotItem.vb.setLimits(xMin=min(self.x_axis_data)-0.01, xMax=max(self.x_axis_data),yMin=min(self.data_amplitude) - 0.2, yMax=max(self.data_amplitude) + 0.2)
            self.graphicsView_main.plot(self.x_axis_data,self.data_amplitude)
            if self.interpolationSelector.currentText()=='Polynomial':
                self.interpolate_the_curve(order_val)
            elif self.interpolationSelector.currentText()=='Spline':
                self.splineInterpolation()  
            elif self.interpolationSelector.currentText()=='Cubic':
                self.CubicInterpolation()  
    
    def hide_polynomial(self):

        self.extrapolationSlider.hide()
        self.chunkSlider.hide()
        self.orderSlider.hide()
        self.textBrowser_5.hide()
        self.textBrowser_6.hide()
        self.textBrowser_7.hide()

    def show_polynomial(self):
        self.extrapolationSlider.show()
        self.chunkSlider.show()
        self.orderSlider.show()
        self.textBrowser_5.show()
        self.textBrowser_6.show()
        self.textBrowser_7.show()        

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
            self.coeffs,residual, _, _, _= np.polyfit(t[0:interpol_range], data[0:interpol_range], interpol_order, full=True)
            if residual.size != 0:
                self.residuals.append(residual[0])
            self.chunk_coeffs.append(self.coeffs)

            p = np.poly1d(self.coeffs)
            self.graphicsView_main.plot(t,p(t),pen = self.blue_pen)

    def splineInterpolation(self):
        amplitude=self.data_amplitude
        interpolationEquation= make_interp_spline(self.x_axis_data,amplitude,2)
        time=np.linspace(0,self.x_axis_data.max(),500)
        self.graphicsView_main.plot(time,interpolationEquation(time),pen = self.blue_pen)

    def CubicInterpolation(self):
        amplitude=self.data_amplitude
        interpolationEquation= CubicSpline(self.x_axis_data,amplitude)
        time=np.linspace(0,self.x_axis_data.max(),500)
        self.graphicsView_main.plot(time,interpolationEquation(time),pen = self.blue_pen)
    
    def interpolation_method(self):
        if self.interpolationSelector.currentText()=='Polynomial' :
                self.show_polynomial()
                self.plot_data(self.intial_slider_order_val)
        elif self.interpolationSelector.currentText()=='Spline' :
                self.hide_polynomial()  
                self.plot_data(self.intial_slider_order_val)
        elif self.interpolationSelector.currentText()=='Cubic' :
                self.hide_polynomial()  
                self.plot_data(self.intial_slider_order_val)
        
    def orderChange(self):
        self.intial_slider_order_val = int(self.orderSlider.value())
        self.plot_data(self.intial_slider_order_val)
        self.Latex_Equation(self.intial_slider_order_val)

    def Latex_Equation(self, slider_order_val):
        chunck_number = self.chunkSlider.value()
        residual = self.residuals[chunck_number - 1]
        self.eqn = []
        for s in range (chunck_number):
            eqn12 = 'y = '
            order = slider_order_val
            coeffs = self.chunk_coeffs[s]
            for i in range(slider_order_val + 1):
                if order == 0 :
                    eq1 = '{}\cdot'.format( round(coeffs[i],2))
                    eqn12 = eqn12 + eq1 
                else : 
                    eq1 = '{}\cdot x^{}'.format( round(coeffs[i],2), order)
                    eqn12 = eqn12 + eq1 + ' + ' 
                order -= 1
            self.eqn.append(eqn12)
        latex_equation =  '$'+ self.eqn [chunck_number - 1] + '$'
        self.fig.suptitle(latex_equation, fontsize = 10, x=0.0, y=0.5, horizontalalignment='left', verticalalignment='center')
        self.canvas.draw()
        self.errors = []
        for s in range (chunck_number): 
            residual = self.residuals[s -1]
            error = math.sqrt(residual)
            error_latex = '$Error = {} \%$ '.format(round(error*100,1))
            self.errors.append(error_latex)
        self.fig_error.suptitle(self.errors[chunck_number - 1], x=0.0, y=0.5, horizontalalignment='left', verticalalignment='center')
        self.canvas_error.draw()

    def latexeqn(self):
        Chunk_no = int (self.comboBox.currentText())
        latex_equation =  '$'+ self.eqn [ int(Chunk_no) - 1] + '$'
        self.fig.suptitle(latex_equation, fontsize = 10, x=0.0, y=0.5, horizontalalignment='left', verticalalignment='center')
        self.canvas.draw()
        self.fig_error.suptitle(self.errors[Chunk_no- 1], x=0.0, y=0.5, horizontalalignment='left', verticalalignment='center')
        self.canvas_error.draw()
        
        self.errors = []
        for s in range (chunck_number): 
            residual = self.residuals[s -1]
            error = math.sqrt(residual)
            error_latex = '$Error = {} \%$ '.format(round(error*100,1))
            self.errors.append(error_latex)
        self.fig_error.suptitle(self.errors[chunck_number - 1], x=0.0, y=0.5, horizontalalignment='left', verticalalignment='center')
        self.canvas_error.draw()
        
        
    def chunkChange(self):
        self.comboBox.clear()
        self.slider_chunk_val = self.chunkSlider.value()
        self.chunk_size = ceil(1000 / self.slider_chunk_val)
        self.plot_data(self.intial_slider_order_val)
        for i in range(self.slider_chunk_val):
            self.comboBox.addItem(str(self.slider_chunk_val - i))
        
        self.errors = []
        for s in range (chunck_number): 
            residual = self.residuals[s -1]
            error = math.sqrt(residual)
            error_latex = '$Error = {} \%$ '.format(round(error*100,1))
            self.errors.append(error_latex)
        self.fig_error.suptitle(self.errors[chunck_number - 1], x=0.0, y=0.5, horizontalalignment='left', verticalalignment='center')
        self.canvas_error.draw()

    def error_map(self):
    
        if self.pushButton.text() != "Generate Error Map":
            self.progressBar.setValue(0)
            self.pushButton.setText("Generate Error Map")
            if self.bool_heatmap == 1:
                self.canvas1.hide()
            return

        self.pushButton.setText("Cancel")
        self.progressBar.show()
        comboY =self.comboBox_3.currentText()
        comboX =self.comboBox_2.currentText()
        no_chuncks = 5
        degree_value = 5
        overlapping = 0.75
        overlaprange = 5
        chunck_label = list(map(str, range(1, no_chuncks + 1)))
        degree_label = list(map(str, range(1, degree_value + 1)))
        overlapping_label = [f"{overlapping_index}%" for overlapping_index in range(5, int(overlaprange*5+5), 5)]

        overlapping_values, overlap = [], 1
        while overlap > overlapping:
            overlap -= .05
            overlapping_values.append(overlap)
        self.start_progress_bar() 
        if (comboX == "Order of polynomial" and comboY == "no. of chunks") or  (comboX == "no. of chunks" and comboY == "Order of polynomial") :
            matrix1 = []
            for i in range(1, no_chuncks+1):
                matrix1.append([])
                for j in range(degree_value):
                        X_ErrorMap = self.calculate_chuncks(self.x_axis_data, i, overlapping)
                        Y_ErrorMap = self.calculate_chuncks(self.data_amplitude, i, overlapping)
                        errors = []
                        for k in range(i):
                            x_map_val = X_ErrorMap[k]
                            y_map_val = Y_ErrorMap[k]
                            error_x = self.get_error(x_map_val,y_map_val,j)
                            errors.append(error_x)
                        matrix1[i-1].append(np.average(errors))

            matrix1 = np.array(matrix1)[::-1]


            if comboX == "no. of chunks" and comboY == "Order of polynomial":
                normalized_error_1=self.get_invers(matrix1)
                normalized_error_1=self.normalization(normalized_error_1)
                fig, self.ax = plt.subplots(figsize=(1, 1))
                self.ax = sns.heatmap(normalized_error_1 , xticklabels=chunck_label, yticklabels=degree_label[::-1])
            else:
                normalized_error_1=self.normalization(matrix1)
                fig, self.ax = plt.subplots(figsize=(1, 1))
                self.ax = sns.heatmap(normalized_error_1 , xticklabels=degree_label, yticklabels=chunck_label[::-1])

            self.toggle_errormap(fig)


        elif (comboX == "Order of polynomial" and comboY == "Over lapping") or (comboX == "Over lapping" and comboY == "Order of polynomial") :
            matrix2=[]

            for i in range(degree_value):
                matrix2.append([])
                for j in range(len(overlapping_values)):
                        X_Error_Map = self.calculate_chuncks(self.x_axis_data,no_chuncks,overlapping_values[j])
                        Y_Error_Map = self.calculate_chuncks(self.data_amplitude,no_chuncks,overlapping_values[j])
                        x1_map_val,y1_map_val= X_Error_Map[0],Y_Error_Map[0]
                        x2_map_val,y2_map_val = X_Error_Map[1],Y_Error_Map[1]
                        error_x1 = self.get_error(x1_map_val,y1_map_val,i)
                        error_x2 = self.get_error(x2_map_val,y2_map_val,i)
                        matrix2[i].append((error_x1+error_x2)/2)
            matrix2 = np.array(matrix2)[::-1]

            if comboX == "Over lapping" and comboY == "Order of polynomial":
                normalized_error_2=self.get_invers(matrix2)                
                normalized_error_2=self.normalization(normalized_error_2)
                fig, self.ax = plt.subplots(figsize=(1, 1))
                self.ax = sns.heatmap(normalized_error_2 , xticklabels=overlapping_label, yticklabels=degree_label[::-1])
            else:
                normalized_error_2=self.normalization(matrix2)
                fig, self.ax = plt.subplots(figsize=(1, 1))
                self.ax = sns.heatmap(normalized_error_2 , xticklabels=degree_label, yticklabels=overlapping_label[::-1])

            self.toggle_errormap(fig)


        elif (comboX == "no. of chunks" and comboY == "Over lapping") or  (comboX == "Over lapping" and comboY == "no. of chunks"):

            matrix3 = []
            for i in range(1,no_chuncks+1):
                matrix3.append([])
                for j in range(len(overlapping_values)):
                        X_Error_Map = self.calculate_chuncks(self.x_axis_data, i, overlapping_values[j])
                        Y_Error_Map = self.calculate_chuncks(self.data_amplitude, i, overlapping_values[j])
                        errors = []
                        for k in range(i):
                            x_error_val = X_Error_Map[k]
                            y_error_val = Y_Error_Map[k]
                            error_x = self.get_error(x_error_val,y_error_val,degree_value)
                            errors.append(error_x)
                        matrix3[i-1].append(np.average(errors))
            matrix3 = np.array(matrix3)[::-1]

            if (comboX == "Over lapping" and comboY == "no. of chunks"):
                normalized_error_3=self.get_invers(matrix3)
                normalized_error_3=self.normalization(normalized_error_3)
                fig, self.ax = plt.subplots(figsize=(1, 1))
                self.ax = sns.heatmap(normalized_error_3, xticklabels=overlapping_label, yticklabels=chunck_label[::-1])
            else:
                normalized_error_3=self.normalization(matrix3)
                fig, self.ax = plt.subplots(figsize=(1, 1))
                self.ax = sns.heatmap(normalized_error_3, xticklabels=chunck_label, yticklabels=overlapping_label[::-1])

            self.toggle_errormap(fig)

        else:
            self.progressBar.hide()
            print("You can't get The error map between the same values")
            self.pushButton.setText("Generate Error Map")
    
    def calculate_chuncks(self,Array_A,no_chunks,overlap_per):
        size = int(1000 / no_chunks)
        step = int(overlap_per * size)
        Array_A = [Array_A[i: i + size] for i in range(0, len(Array_A), step)]
        return Array_A
    
    def get_error(self,x,y,i):
        z_chunk1, residual, _, _, _ = np.polyfit(x, y, i, full=True)
        avgerror =math.sqrt(residual[0])
        return(avgerror)

    def toggle_errormap (self, fig):
        if self.bool_heatmap == 0:
            self.canvas1 = FigureCanvasQTAgg(fig)
            self.splitter_AllGraphs.addWidget(self.canvas1)
            self.bool_heatmap = 1
        else:
            self.canvas1.hide()
            self.canvas1 = FigureCanvasQTAgg(fig)
            self.splitter_AllGraphs.addWidget(self.canvas1)

    def extrapolation_change(self):
        self.chunkSlider.setValue(0)
        self.chunk_size = 1000
        self.slider_chunk_val=1
        self.extrapolation_sliderval = self.extrapolationSlider.value()
        val = self.extrapolation_sliderval-1
        self.extrapolation_pecentage = 100-val*10
        slider_order_val = self.orderSlider.value()
        self.plot_data(slider_order_val)

    def conection(self):
        self.comboBox_3.clear()
        self.comboBox_3.addItem("Order of polynomial")
        self.comboBox_3.addItem("no. of chunks")
        self.comboBox_3.addItem("Over lapping")
        cureentindex=self.comboBox_3.findText(self.comboBox_2.currentText())
        self.comboBox_3.removeItem(cureentindex)

    def conection2(self):
        self.comboBox_2.clear()
        self.comboBox_2.addItem("Order of polynomial")
        self.comboBox_2.addItem("no. of chunks")
        self.comboBox_2.addItem("Over lapping")
        cureentindex=self.comboBox_2.findText(self.comboBox_3.currentText())
        self.comboBox_2.removeItem(cureentindex)      

    def start_progress_bar(self):
        self.thread = MyThread()
        self.thread.change_value.connect(self.set_progress_val)
        self.thread.start()     

    def set_progress_val(self, val):
        self.progressBar.setValue(val)

    def normalization(self,oldmatrix):
        normalized_error = []
        min = np.amin(oldmatrix)
        max = np.amax(oldmatrix)

        for i in oldmatrix:
            normalized_error_temp = []
            for j in i:
                value = (j - min) / (max - min)
                normalized_error_temp.append(value)
            normalized_error.append(normalized_error_temp) 
        return normalized_error

    def get_invers(self,matrixIN):
                matrixIN = matrixIN.T
                # for n in range(len(matrix3[m])):
                # for m in range(len(matrix3[0])):
                matrixOUT=[]
                matrixOUT = np.array(matrixIN)[::-1]
                matrixOUT[4,:]=matrixIN[0,:]  
                matrixOUT[0,:]=matrixIN[4,:]
                matrixOUT[3,:]=matrixIN[1,:]
                matrixOUT[1,:]=matrixIN[3,:]
                matrixOUT[2,:]=matrixIN[2,:]

                matrixIN[4,:]=matrixOUT[4,:]  
                matrixIN[0,:]=matrixOUT[0,:]
                matrixIN[3,:]= matrixOUT[3,:]
                matrixIN[1,:]= matrixOUT[3,:]
                matrixIN[2,:]= matrixOUT[2,:]
            
                matrixOUT[:,4]=matrixIN[:,0]  
                matrixOUT[:,0]=matrixIN[:,4]
                matrixOUT[:,3]=matrixIN[:,1]
                matrixOUT[:,1]=matrixIN[:,3]
                matrixOUT[:,2]=matrixIN[:,2]      

                return matrixOUT 

    # def start_progress_bar(self):
    #      self.thread = MyThread()
    #      self.thread.change_value.connect(self.set_progress_val)
    #      self.thread.start()
        


        
def main ():
    app = QApplication(sys.argv)
    window = MainApp ()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()