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
import pygame as pyg
import sf2_loader as sf
import playpiano as pp
import playdrums as pd

FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"qtFiles/main.ui"))

new_sig=[]
t = np.arange(0, 1, 0.001)

class MainApp(QMainWindow , FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI()
        pyg.mixer.init()
        pyg.init()

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
