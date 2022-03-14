##PyQT5
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
from PyQt5 import QtCore, QtGui, QtWidgets,QtPrintSupport
from PyPDF2.pdf import PdfFileReader
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.Qt import QFileInfo
import matplotlib.pyplot as plt
from numpy.lib.function_base import append
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_pdf import PdfPages, _create_pdf_info_dict
from PyPDF2 import PdfFileMerger, merger
import fitz
import pyqtgraph.exporters

root = Tk()
root.title('Codemy.com - Learn To Code!')

FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"main.ui"))


class MainApp(QMainWindow , FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI()
        
        self.cmap = 'inferno'
        self.title = ''
        self.counter = 0
        self.max_len = 0
        self.Signal_Flag = 1
        self.First_Signal_Flag = 0
        self.Second_Signal_Flag = 0
        self.Third_Signal_Flag = 0
        self.speed=1000
        self.isRunning=True

        self.Hide_First_Signal_Flag = 0
        self.Hide_Second_Signal_Flag = 0
        self.Hide_Third_Signal_Flag = 0
        
        self.min = -100
        self.max = -50
        self.pen1 = pg.mkPen('r')
        self.pen2 = pg.mkPen('b')
        self.pen3 = pg.mkPen('y')

    def Handle_UI(self):
        # self = QMainWindow
        self.setWindowTitle('Multi-Channel Signal Viewer')
        self.Handle_Buttons()
        # self.Handle_GraphicsViews()
        # self.Handle_Slider()

    def Handle_Buttons(self):
        
        self.BrowseButton_13.clicked.connect(self.Browse)
        self.ShowcomboBox.currentTextChanged.connect(self.Show)
        self.HidecomboBox.currentTextChanged.connect(self.Hide)
        self.PauseButton_6.clicked.connect(self.Pause)
        self.PlayButton_7.clicked.connect(self.Play)
        self.currSpecFigure=0

        # Zoom Button Functions
        self.zoomInButton.clicked.connect(self.zoomIn)
        self.zoomOutButton.clicked.connect(self.zoomOut)
        
        self.Slidermax.setMinimum(-75)
        self.Slidermax.setMaximum(-25)
        self.Slidermax.setValue(-50)
        self.Slidermax.setTickInterval(12)
        self.Slidermax.setTickPosition(QSlider.TicksBelow)
        self.Slidermax.valueChanged.connect(self.Contrast_max_change)

        self.Slidermin.setMinimum(-150)
        self.Slidermin.setMaximum(-75)
        self.Slidermin.setValue(-100)
        self.Slidermin.setTickInterval(12)
        self.Slidermin.setTickPosition(QSlider.TicksBelow)
        self.Slidermin.valueChanged.connect(self.Contrast_min_change)

        # Speed Slider
        self.speedSlider.setMinimum(-50)
        self.speedSlider.setMaximum(50)
        self.speedSlider.setValue(-10)
        self.speedSlider.setTickPosition(QSlider.TicksBelow)
        self.speedSlider.setSingleStep(1)
        self.speedSlider.valueChanged.connect(self.Slider)

        # Scroll Slider Functions
        self.horizontalScroll.valueChanged.connect(self.scrollHorizontal)
        self.horizontalScroll.sliderMoved.connect(self.scrollHorizontal)
        self.horizontalScroll.sliderReleased.connect(self.scrollHorizontal)
        self.verticalScroll.valueChanged.connect(self.scrollVertical)
        self.verticalScroll.sliderMoved.connect(self.scrollVertical)
        self.verticalScroll.sliderReleased.connect(self.scrollVertical)

        self.ExportButton_12.clicked.connect(self.Export)
        self.SpectrogramcomboBox.currentTextChanged.connect(self.Spectrogram)
        self.ColorcomboBox.currentTextChanged.connect(self.spectroColor)
        
        self.titleButton.clicked.connect(self.addTitle)
        self.titleConfirmButton.clicked.connect(self.confirmTitle)

        
        
        

#----------------------------------------------------------------------------------------------------------#
    # Utility functions (Play/Pause, Zoom, Show/Hide, Scroll, Title)
    
    def Slider(self):
        self.speed=self.speed+self.speedSlider.value()

        if(self.speed > 0):
            self.timer.setInterval(self.speed)
            self.timer.timeout.connect(self.update_plot_data)
            self.timer.start()

    def Pause(self):
            self.isRunning=False        
    
    def Play(self):
            self.isRunning=True   

    def zoomIn(self):
        self.Pause
        self.graphicsView.plotItem.getViewBox().scaleBy((0.85,0.85))

    def zoomOut(self):
        self.Pause
        self.graphicsView.plotItem.getViewBox().scaleBy((1.15,1.15))

    def scrollHorizontal(self):
            self.horizontalScroll.setMaximum(self.counter)
            self.horizontalScroll.setMinimum(0)
            val = self.horizontalScroll.value()
            self.graphicsView.setXRange(val-50, val+50)

    def scrollVertical(self):
            self.verticalScroll.setMaximum(int(self.maxAmp))
            self.verticalScroll.setMinimum(int(self.minAmp))
            val = self.verticalScroll.value()
            self.graphicsView.setYRange(val-((self.maxAmp-self.minAmp) / 5), val+((self.maxAmp-self.minAmp) / 5))

    def confirmTitle(self):
        self.title = self.titleText.toPlainText()
        self.titleText.setText('')
        self.titleLabel.setText(self.title)
        self.titleText.setEnabled(False)
        self.titleConfirmButton.setEnabled(False)

    def addTitle(self):
        self.titleText.setEnabled(True)
        self.titleConfirmButton.setEnabled(True)

    def Show(self) :
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


    def Hide(self):
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

#----------------------------------------------------------------------------------------------------------#
    # Signal Plotting (Browse, Timer, Update Plot)

    def Browse(self):
        open_place = QFileDialog.getOpenFileName(self , caption= "Browse", directory=".", filter="All Files (*.*)")
        path = open_place[0].split(',') 
        myfile = open(path[0], "r") #path refears to the chosen file after splitting   # 'r' refears to the mode, the mode here is reading 
        self.amplitude = []
        self.time = []
        self.sigDatax=[]
        self.sigDatay=[]
        while myfile:
            myline  = myfile.readline()
            if myline == "":  break
            self.line = myline.split() 
            self.amplitude.append(float(self.line [0]))
            self.time.append(float(self.line [1])) 
        myfile.close()
        if self.Signal_Flag == 1:
            self.channel1_path=path
            self.x1 = np.array(self.time)
            self.y1 = np.array(self.amplitude)
            self.maxAmp = max(self.y1)
            self.minAmp = min(self.y1)
            self.sigDatax.append(self.x1)
            self.sigDatay.append(self.y1)
            if (self.maxAmp - self.minAmp) < 5:
                self.y1*=10
                self.maxAmp = max(self.y1)
                self.minAmp = min(self.y1)
            self.Signal_Flag = 2
            self.First_Signal_Flag = 1
        elif self.Signal_Flag == 2:
            self.channel2_path=path

            self.x2 = np.array(self.time)
            self.y2 = np.array(self.amplitude)
            self.sigDatax.append(self.x2)
            self.sigDatay.append(self.y2)

            if (max(self.y2) - min(self.y2)) < 5:
                self.y2*=10
            if max(self.y2) > self.maxAmp:
                self.maxAmp = max(self.y2)
            if min(self.y2) < self.minAmp:
                self.minAmp = min(self.y2)
            self.Second_Signal_Flag = 1
            self.Signal_Flag = 3
        elif self.Signal_Flag == 3:
            self.channel3_path=path
            self.x3 = np.array(self.time)
            self.y3 = np.array(self.amplitude)
            self.sigDatax.append(self.x3)
            self.sigDatay.append(self.y3)

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
        self.timer.setInterval(self.speed)                       #In control of speed :)
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
        print(self.max)
        if self.counter < self.max_len:                                                    #To stop at the limit of the graph
            if self.counter < 100:
                start_count = 0
                end_count = 100
            else:
                start_count = self.counter - 100
                end_count = self.counter
                self.graphicsView.setXRange(start_count,end_count)
                self.graphicsView.setYRange(self.minAmp, self.maxAmp)
    
#----------------------------------------------------------------------------------------------------------#
    # Data Exporting

    def table_creation(self, pdffilename):
        table_header = ["Signal Name", "Mean", "Standard Deviation", "Maximum Value", "Minimum Value", 'duration']
        table_data = [table_header]

        chn = [self.HidecomboBox.itemText(0), self.HidecomboBox.itemText(1), self.HidecomboBox.itemText(2)]
        for i in range(1):
            amplitude = self.sigDatay[i]
            time = self.sigDatax[i]
            print(amplitude)
            signal_info=["{}".format(chn[i]),round(amplitude.mean(),5),round(amplitude.std(),5),round(amplitude.max(),5),round(amplitude.min(),5),round((time.max() - time.min()),5)]
            table_data.append(signal_info)

        fig = plt.figure(constrained_layout=True)
        fig.patch.set_visible(False)
        fig, ax = plt.subplots()
        ax.axis('off')
        ax.axis('tight')
        table = ax.table(cellText=table_data, loc='center')
        table.scale(1, 2)
        fig.tight_layout()
        fileName = pdffilename + ".pdf"
        report = PdfPages(pdffilename)
        report.savefig()
        #plt.close
        report.close()

    def print_widget(self,Plotting_Weidget ,pdf_filename):
        ex=pg.exporters.ImageExporter(self.graphicsView.plotItem)
        ex.export("test1.png")
        # ex = pg.exporters.ImageExporter(self.frame_3.paintEvent)
        # ex.export("test2.png")
        doc = fitz.open(pdf_filename)  # open the PDF
        img1 = open("test1.png", "rb").read()
        rect1 = fitz.Rect(20, 30, 450, 110)# where to put image: use upper left corner
        
        for page in doc:
            page.insert_image(rect1, stream=img1)

        doc.saveIncr()
    
    def Export(self):
        fn, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Export PDF", None, "PDF files (.pdf);;All Files()")
        if fn != '':
            if QtCore.QFileInfo(fn).suffix() == "": fn += '.pdf'
            self.table_creation(fn)
            self.print_widget(self.graphicsView, fn)

#----------------------------------------------------------------------------------------------------------#
    # Spectrogram Functions

    def Contrast_max_change(self):
        self.max = self.Slidermax.value()
        self.widget.canvas.axes.clear()
        self.item = self.SpectrogramcomboBox.currentText()

        if self.item == "Signal_1":
            self.Fig1 = self.widget.canvas.axes.specgram(self.y1, cmap = self.cmap,xextent =(self.min, self.max))
            self.widget.canvas.draw()
        elif self.item == "Signal_2":
            self.Fig2 = self.widget.canvas.axes.specgram(self.y2, cmap = self.cmap,xextent =(self.min, self.max))
            self.widget.canvas.draw()
        elif self.item == "Signal_3":
            self.Fig3 = self.widget.canvas.axes.specgram(self.y2, cmap = self.cmap,xextent =(self.min, self.max))
            self.widget.canvas.draw()

    def Contrast_min_change(self):
        self.min = self.Slidermin.value()
        self.widget.canvas.axes.clear()

        if self.item == "Signal_1":
            self.Fig1 = self.widget.canvas.axes.specgram(self.y1, cmap = self.cmap,xextent =(self.min, self.max))
            self.widget.canvas.draw()
        elif self.item == "Signal_2":
            self.Fig2 = self.widget.canvas.axes.specgram(self.y2, cmap = self.cmap,xextent =(self.min, self.max))
            self.widget.canvas.draw()
        elif self.item == "Signal_3":
            self.Fig3 = self.widget.canvas.axes.specgram(self.y2, cmap = self.cmap,xextent =(self.min, self.max))
            self.widget.canvas.draw()

    def Spectrogram(self):

        self.widget.canvas.axes.clear()
        self.item = self.SpectrogramcomboBox.currentText()
        fs = int(1 / 0.004)

        if self.item == "Signal_1" :
            self.Fig1 = self.widget.canvas.axes.specgram(self.y1, cmap=self.cmap , xextent =(self.min, self.max))
        elif self.item == "Signal_2" :
            self.Fig2 = self.widget.canvas.axes.specgram(self.y2, cmap = self.cmap, xextent =(self.min, self.max))
        elif self.item == "Signal_3" :
            self.Fig3= self.widget.canvas.axes.specgram(self.y2, cmap = self.cmap, xextent =(self.min, self.max))

        self.widget.canvas.draw()

    def spectroColor(self):

        self.cmap = self.ColorcomboBox.currentText()
        self.Spectrogram()
    
#----------------------------------------------------------------------------------------------------------#

def main ():
    app = QApplication(sys.argv)
    window = MainApp ()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main()
