# -*- coding: utf-8 -*-
"""
Created on Wed May  2 20:32:16 2018

@author: jaymz
"""

import sys
from PyQt4 import QtCore, QtGui
from form import Ui_Dialog

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np

import random

import sounddevice as sd

class MyDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.sampleRate = 44100        
        
        self.ui = Ui_Dialog()
        
        #--------
        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
        #--------        
        
        self.ui.setupUi(self)
        
        self.ui.plot_layout.addWidget(self.toolbar)
        self.ui.plot_layout.addWidget(self.canvas)
        
        self.ui.scanButton.clicked.connect(self.scan)
        
    def plotClear(self, data):
        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.clear()

        # plot data
        ax.plot(data)

        # refresh canvas
        self.canvas.draw()
    def plotAppend(self, data):
        # create an axis
        ax = self.figure.add_subplot(111)
        # plot data
        ax.plot(data)
        # refresh canvas
        self.canvas.draw()
    def plotTriple(self, dat1,dat2,dat3):
        ax1 = self.figure.add_subplot(311)        
        # discards the old graph
        ax1.clear()
        
        ax1.plot(dat1)

        # plot data
        ax2 = self.figure.add_subplot(312,sharex=ax1)
        ax2.plot(dat2)
        
        ax3 = self.figure.add_subplot(313,sharex=ax1)
        ax3.plot(dat3)
        

        # refresh canvas
        self.canvas.draw()
        
    def generateTimeAxis(self,scanTime):
        return np.linspace(0,scanTime,scanTime*self.sampleRate)
        
    def generateFreqSweep(self,startFreq, stopFreq, scanTime, gain):
        t = self.generateTimeAxis(scanTime)
        freq = startFreq + (stopFreq - startFreq)/2/scanTime*t
        return gain*np.sin(2*np.pi*freq*t)
        
    def freqScan(self,startFreq, stopFreq, scanTime, gain):
        audioSignal = self.generateFreqSweep(startFreq,stopFreq,scanTime,gain)
        #self.plotClear(audioSignal)
        recording = sd.playrec(audioSignal, samplerate=self.sampleRate, channels = 2)
        sd.wait()
        #self.plotAppend(recording)
        self.plotTriple(audioSignal,recording[:,0],recording[:,1])        
        
        return recording
        
    def scan(self):
        self.freqScan(self.ui.startFreq_box.value(), self.ui.stopFreq_box.value(), self.ui.scanTime_box.value(), self.ui.gainSlider.value()*1.0/100)
    
 
if __name__ == "__main__":
        app = QtGui.QApplication(sys.argv)
        myapp = MyDialog()
        myapp.show()
        sys.exit(app.exec_())