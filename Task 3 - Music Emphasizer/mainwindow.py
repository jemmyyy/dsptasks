##PyQT5
from fileinput import filename
import string
import queue
from subprocess import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget,plot
from PyQt5 import QtCore
import os 
import matplotlib.ticker as ticker
import sounddevice as sd
import pyqtgraph as pg
from os import path, remove 
import numpy as np
import pandas as pd
import math  
import simpleaudio as sa
import vlc
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg 
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft
from scipy import signal 
from tkinter import filedialog
from tkinter import *
import sys
import pygame as pyg
import sf2_loader as sf
import playpiano as pp
import playdrums as pd

FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"qtFiles/main.ui"))

# new_sig=[]
# t = np.arange(0, 1, 0.001)

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        fig.tight_layout()

class Worker(QtCore.QRunnable):

    def __init__(self, function, *args, **kwargs):
        super(Worker, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):

        self.function(*self.args, **self.kwargs)
class MainApp(QMainWindow , FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI()
        pyg.mixer.init()
        pyg.init()
      
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 60, 511, 331))
        self.splitter_graphs = QtWidgets.QSplitter(self.tab_3)
        self.splitter_graphs.setGeometry(QtCore.QRect(110, 70, 951, 331))
        self.splitter_graphs.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_graphs.setObjectName("splitter_graphs")
        self.gridLayout.addWidget(self.splitter_graphs,0,1,6,4)
        
        self.canvas = MplCanvas(self, width=4, height=4, dpi=100)
        self.splitter_graphs.addWidget(self.canvas)

        self.reference_plot = None
        self.que = queue.Queue(maxsize=20)
        self.downsample = 10
        self.device = 0
        self.channels = [1]
        self.threadpool = QtCore.QThreadPool()
        self.isRunning = False

        deviceInfo = sd.query_devices(self.device)
        self.samplerate = deviceInfo['default_samplerate']
        self.window_length = 200

        length = int(self.window_length*self.samplerate/(1000*self.downsample))
        self.plotdata = np.zeros((length, len(self.channels)))
        sd.default.samplerate = self.samplerate

        self.update_plot()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(30)  # msec
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()



    def Handle_UI(self):
        self.setWindowTitle('Sampling-Theory Illustrator')
        self.Handle_Buttons()

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
        self.pianoButton1.clicked.connect(pp.playPianoNote1_1)
        self.pianoButton1_2.clicked.connect(pp.playPianoNote1_2)
        self.pianoButton1_3.clicked.connect(pp.playPianoNote1_3)
        self.pianoButton1_4.clicked.connect(pp.playPianoNote1_4)
        self.pianoButton1_5.clicked.connect(pp.playPianoNote1_5)
        self.pianoButton1_6.clicked.connect(pp.playPianoNote1_6)
        self.pianoButton1_7.clicked.connect(pp.playPianoNote1_7)
        self.pianoButton2_1.clicked.connect(pp.playPianoNote2_1)
        self.pianoButton2_2.clicked.connect(pp.playPianoNote2_2)
        self.pianoButton2_3.clicked.connect(pp.playPianoNote2_3)
        self.pianoButton2_4.clicked.connect(pp.playPianoNote2_4)
        self.pianoButton2_5.clicked.connect(pp.playPianoNote2_5)

        self.triangleButton.clicked.connect(playTriangle)

        self.drumButtonChina1.clicked.connect(pd.playDrumChina1)
        self.drumButtonChina2.clicked.connect(pd.playDrumChina2)
        self.drumButtonCrash1.clicked.connect(pd.playDrumCrash1)
        self.drumButtonCrash2.clicked.connect(pd.playDrumCrash2)
        self.drumButtonHats1.clicked.connect(pd.playDrumHats1)
        self.drumButtonHats2.clicked.connect(pd.playDrumHats2)
        self.drumButtonRide.clicked.connect(pd.playDrumRide)
        self.drumButtonSplash.clicked.connect(pd.playDrumSplash)
        self.drumButtonStax.clicked.connect(pd.playDrumStax)
        self.drumButtonTom1.clicked.connect(pd.playDrumTom1)
        self.drumButtonTom2.clicked.connect(pd.playDrumTom2)
        self.drumButtonTom3.clicked.connect(pd.playDrumTom3)
        self.drumButtonTom4.clicked.connect(pd.playDrumTom4)
        self.drumButtonTom5.clicked.connect(pd.playDrumTom5)
        self.drumButtonSnare.clicked.connect(pd.playDrumSnare)
        self.VolumeverticalSlider.setMinimum(0)
        self.VolumeverticalSlider.setMaximum(200)
        self.VolumeverticalSlider.setValue(100)
        self.VolumeverticalSlider.setTickInterval(20)
        self.VolumeverticalSlider.setSingleStep(20)
        self.VolumeverticalSlider.setTickPosition(QSlider.TicksRight)
        self.VolumeverticalSlider.valueChanged.connect(self.changeVolume)  
        self.BrowsepushButton.clicked.connect(self.Browse)
        self.PauseButton.clicked.connect(self.Pause)
        self.PlayButton.clicked.connect(self.Play)

    def Browse(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, 'Open Song', QtCore.QDir.rootPath(), 'wav(*.wav)')

        self.media = vlc.MediaPlayer(filePath)
        self.media.play()

        worker = Worker(self.start_stream,)
        self.threadpool.start(worker)


    def start_stream(self):
        def audio_callback(indata, frames, time, status):
            self.que.put(indata[::self.downsample, [0]])
        stream = sd.InputStream(device=self.device, channels=max(
            self.channels), samplerate=self.samplerate, callback=audio_callback)
        with stream:
            input()

    def update_plot(self):
        try:
            data = [0]

            while True:
                try:
                    data = self.que.get_nowait()
                except queue.Empty:
                    break
                shift = len(data)
                self.plotdata = np.roll(self.plotdata, -shift, axis=0)
                self.plotdata[-shift:, :] = data
                self.ydata = self.plotdata[:]
                self.canvas.axes.set_facecolor((0, 0, 0))

                if self.reference_plot is None:
                    plot_refs = self.canvas.axes.plot(
                        self.ydata, color=(0, 1, 0.29))
                    self.reference_plot = plot_refs[0]
                else:
                    self.reference_plot.set_ydata(self.ydata)

            
            self.canvas.axes.yaxis.grid(True, linestyle='--')
            self.canvas.axes
            self.canvas.axes.yaxis.grid(True, linestyle='--')
            start, end = self.canvas.axes.get_ylim()
            self.canvas.axes.yaxis.set_ticks(np.arange(start, end, 0.1))
            self.canvas.axes.yaxis.set_major_formatter(
                ticker.FormatStrFormatter('%0.1f'))
            self.canvas.axes.set_ylim(ymin=-0.5, ymax=0.5)
            if self.isRunning == False:
                self.canvas.draw()
        except:
            pass

    def Pause(self):
        self.isRunning=True
        self.media.pause()
    
    def Play(self):
        self.isRunning=False
        self.media.play()
    
    def changeVolume(self):
        SliderValue=int(self.VolumeverticalSlider.value())
        self.media.audio_set_volume(SliderValue)
        pass
        
        
def playTriangle(self):
    sound = pyg.mixer.Sound('Datasests/Triangle Notes/triangle.wav')
    sound.play()

def main ():
    app = QApplication(sys.argv)
    window = MainApp ()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
