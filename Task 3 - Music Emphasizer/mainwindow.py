##PyQT5
from email.mime import base
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
from scipy.io import wavfile
import scipy.io 
import logging

FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"qtFiles/main.ui"))

# new_sig=[]
# t = np.arange(0, 1, 0.001)
class MplCanvas_spec_empty(FigureCanvasQTAgg):
    
    def __init__(self, parent=None, width=4, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set(xlabel='time (sec)', ylabel='frequency (Hz)', title = "Spectrogram" )
        super(MplCanvas_spec_empty, self).__init__(fig)

class Canvas_spec(FigureCanvasQTAgg):
    def __init__(self, amplitude, fs):

        fig, self.ax = plt.subplots(figsize=(5, 4))
        super().__init__(fig)

        """
        Matplotlib Script
        """
        if math.log2(len(amplitude)) >= 256:
            nfft = math.floor(math.log2(len(amplitude)))
        else:
            nfft = 256

        noverlap = int(nfft*0.88)
        self.ax.specgram(amplitude, NFFT=nfft, Fs=fs,noverlap=noverlap, cmap="plasma")

        self.ax.set(xlabel='time (sec)', ylabel='frequency (Hz)', title = "Spectrogram")
        self.ax.grid()    

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
        self.dummyEqualize = QtWidgets.QPushButton(self.tab_3)
        self.dummyEqualize.setObjectName("pushButton")
        self.dummyEqualize.clicked.connect(self.equalize)
        self.gridLayout.addWidget(self.dummyEqualize,5,0,2,2)
        self.dummyEqualize.clicked.connect(self.equalize) 
        self.splitter_graphs = QtWidgets.QSplitter(self.tab_3)
        self.splitter_graphs.setGeometry(QtCore.QRect(20, 70, 1211, 331))
        self.splitter_graphs.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_graphs.setObjectName("splitter_graphs")
        self.gridLayout.addWidget(self.splitter_graphs,0,1,2,1)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.splitter_graphs.addWidget(self.canvas)
        self.emptySpec = MplCanvas_spec_empty(self, width=5, height=4, dpi=100)
        self.splitter_graphs.addWidget(self.emptySpec)
        self.reference_plot = None
        self.que = queue.Queue(maxsize=20)
        self.downsample = 10
        self.device = 0
        self.time=0
        self.channels = [1]
        self.threadpool = QtCore.QThreadPool()
        self.isRunning = False
        self.DisplayedSpecto=False
        
        self.pianoModes=[2,2.5,1.6,1.5,(4/3)]
        self.octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B']

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

        self.drumVerticalSlider.setMaximum(10)
        self.drumVerticalSlider.setMinimum(0)
        self.drumVerticalSlider.setValue(4)
        self.drumVerticalSlider.setTickInterval(1)
        self.drumVerticalSlider.setSingleStep(1)
        self.drumVerticalSlider.setTickPosition(QSlider.TicksRight)

        self.guitarVerticalSlider.setMaximum(10)
        self.guitarVerticalSlider.setMinimum(0)
        self.guitarVerticalSlider.setValue(4)
        self.guitarVerticalSlider.setTickInterval(1)
        self.guitarVerticalSlider.setSingleStep(1)
        self.guitarVerticalSlider.setTickPosition(QSlider.TicksRight)


        self.sticksVerticalSlider.setMaximum(10)
        self.sticksVerticalSlider.setMinimum(0)
        self.sticksVerticalSlider.setValue(1)
        self.sticksVerticalSlider.setTickInterval(1)
        self.sticksVerticalSlider.setSingleStep(1)
        self.sticksVerticalSlider.setTickPosition(QSlider.TicksRight)

        


        self.pianoFreqSlider.setMaximum(280)
        self.pianoFreqSlider.setMinimum(240)
        self.pianoFreqSlider.setValue(260)
        

    def Handle_Buttons(self):
        self.pianoButton1.clicked.connect(lambda: self.playPiano(0))
        self.pianoButton1_2.clicked.connect(lambda: self.playPiano(2))
        self.pianoButton1_3.clicked.connect(lambda: self.playPiano(4))
        self.pianoButton1_4.clicked.connect(lambda: self.playPiano(5))
        self.pianoButton1_5.clicked.connect(lambda: self.playPiano(7))
        self.pianoButton1_6.clicked.connect(lambda: self.playPiano(9))
        self.pianoButton1_7.clicked.connect(lambda: self.playPiano(11))
        self.pianoButton2_1.clicked.connect(lambda: self.playPiano(1))
        self.pianoButton2_2.clicked.connect(lambda: self.playPiano(3))
        self.pianoButton2_3.clicked.connect(lambda: self.playPiano(6))
        self.pianoButton2_4.clicked.connect(lambda: self.playPiano(8))
        self.pianoButton2_5.clicked.connect(lambda: self.playPiano(10))

        self.pianoModeButton.clicked.connect(self.getPianoMode)
        self.pianoFreqSlider.valueChanged.connect(self.getPianoFreq)

        self.triangleButton.clicked.connect(playTriangle)

        self.drumButtonChina1.clicked.connect(pd.playDrumChina1)
        self.drumButtonChina2.clicked.connect(pd.playDrumChina2)
        self.drumButtonChina3.clicked.connect(pd.playDrumHats1)
        self.drumButtonRide.clicked.connect(lambda: self.playDrums(8, 170))
        self.drumButtonTom1.clicked.connect(lambda: self.playDrums(5, 80))
        self.drumButtonTom2.clicked.connect(lambda: self.playDrums(7, 80))
        self.drumButtonTom4.clicked.connect(lambda: self.playDrums(9, 80))
        self.drumButtonSnare.clicked.connect(lambda: self.playDrums(11, 50))

        self.drumModeButton.clicked.connect(self.getDrumMode)

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
        self.ShowSpectrogrampushButton.clicked.connect(self.spectrogram)
        self.musicmixerpushButton.clicked.connect(self.equalize)
        
    def Browse(self):
        self.filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, 'Open Song', QtCore.QDir.rootPath(), 'wav(*.wav)')     
        self.playFile(self.filePath)
        worker = Worker(self.start_stream,)
        self.threadpool.start(worker)    
        
    def playFile(self,filePath):
        self.media = vlc.MediaPlayer(filePath)
        self.media.stop()
        self.media.play()
        self.media.set_time(self.time)
        self.fs, self.data = wavfile.read(filePath)

    def spectrogram(self):
        if self.DisplayedSpecto==False:
            self.emptySpec.hide()
            self.spectrogramFig = Canvas_spec(self.data, self.fs)
            self.splitter_graphs.addWidget(self.spectrogramFig)
            self.DisplayedSpecto=True
        else: 
            self.spectrogramFig.hide()
            self.spectrogramFig = Canvas_spec(self.data, self.fs)
            self.splitter_graphs.addWidget(self.spectrogramFig)        

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
      

    def playDrums(self, index, base_freq):
        mode =  self.getDrumMode()
        self.playKey(index, base_freq, 100, 0.15, mode)

    def playPiano(self, index):
        base_freq = self.getPianoFreq()
        mode = self.getPianoMode()
        self.playKey(index, base_freq, 12, 0.5, mode)

    def getPianoMode(self):
        mode = self.pianoModesComboBox.currentIndex() 
        self.pianoModes=[2,2.5,1.6,1.5,(4/3)]
        return self.pianoModes[mode]

    def getDrumMode(self):
        mode = self.drumModesComboBox.currentIndex() 
        self.drumModes=[2,2.5,1.6,1.5,(4/3)]
        return self.drumModes[mode]

    def getPianoFreq(self):
        freq = self.pianoFreqSlider.value()
        return freq

    def getWave(self, freq, duration):
        amplitude = 4096
        self.samplerate = 44100
        time = np.linspace(0, duration, int(self.samplerate * duration))
        wave = amplitude * np.sin(2 * np.pi * freq * time)
        return wave

    def getNotes(self, base_freq, denominator):
        self.octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B']
        note_freq = {self.octave[note_index]: base_freq * pow(2, (note_index / denominator)) for note_index in
                     range(len(self.octave))}
        return note_freq

    def playKey(self, key_index, base_freq, den, duration, mode):
        base_freq = base_freq * mode
        notesFreqs = self.getNotes(base_freq, den)
        sound = self.octave[key_index]
        song = [self.getWave(notesFreqs[note], duration) for note in sound.split('-')]
        song = np.concatenate(song)
        data = song.astype(np.int16)
        data = data * (16300/np.max(data)) 
        data = song.astype(np.int16)
        sa.play_buffer(data, 1, 2, 44100)


    def equalize(self):
        
        # [drums , guitar , sticks]
        freq_min = [0,2000,1466]
        freq_max = [380, 15000,9337]

        gainChanges = []
        gainChanges.append(self.drumVerticalSlider.value())
        gainChanges.append(self.guitarVerticalSlider.value())
        gainChanges.append(self.sticksVerticalSlider.value())

        self.media.pause()
        self.fs, self.data = wavfile.read(self.filePath)
        self.data = self.data / 2.0 ** 15
        N = len(self.data)
        self.time=self.media.get_time()
        rfft_coeff = np.fft.rfft(self.data)
        frequencies = np.fft.rfftfreq(N, 1. / self.fs)

        for i in range(3):
            minmum=freq_min[i]
            maximum=freq_max[i]
            for j in frequencies:
                if  (minmum> j <maximum):
                    freqSamplingINT=len(frequencies)/(self.fs/2)
                    theindex=round(freqSamplingINT * j )
                    rfft_coeff[theindex] = rfft_coeff[theindex] * gainChanges[i]

        
        Equalized_signal = np.fft.irfft(rfft_coeff)
        scipy.io.wavfile.write('created.wav', self.fs, Equalized_signal)
        self.media.stop()
        self.spectrogram()
        self.playFile('created.wav')
        

    def closeEvent(self,event):
        self.media.stop()
        event.accept()

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
