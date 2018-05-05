# -*- coding: utf-8 -*-
"""
Created on Wed May  2 20:32:16 2018

@author: jaymz
"""

import sys, os
import pickle
from PyQt4 import QtCore, QtGui
from form import Ui_Dialog

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np

import sounddevice as sd

class MyDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.sampleRate = 44100        
        
        self.ui = Ui_Dialog()
        
        #--------
        # a figure instance to plot on
        self.td_figure = Figure()
        self.fa_figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.td_canvas = FigureCanvas(self.td_figure)
        self.fa_canvas = FigureCanvas(self.fa_figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.td_toolbar = NavigationToolbar(self.td_canvas, self)
        self.fa_toolbar = NavigationToolbar(self.fa_canvas, self)
        #--------        
        
        self.ui.setupUi(self)
        
        self.ui.plot_layout.addWidget(self.td_toolbar)
        self.ui.fa_plotLayout.addWidget(self.fa_toolbar)
        self.ui.plot_layout.addWidget(self.td_canvas)
        self.ui.fa_plotLayout.addWidget(self.fa_canvas)
        
        self.ui.scanButton.clicked.connect(self.scan)
        self.ui.analysisButton.clicked.connect(self.plotFreqAnalysis)
        self.ui.saveButton.clicked.connect(self.saveData)
        self.ui.loadButton.clicked.connect(self.loadData)
        
        self.ui.combNumModes_box.valueChanged.connect(self.updateCombStatusText)
        self.ui.combNumCycles_box.valueChanged.connect(self.updateCombStatusText)
        self.updateCombStatusText()
        
        print self.ui.analysisMethod_box.currentIndex()
        
    def plotClear(self,fig,canv, data, x=None):
        # create an axis
        ax = fig.add_subplot(111)

        # discards the old graph
        ax.clear()

        # plot data
        if(x==None):
            ax.plot(data)
        else:
            ax.plot(x,data)

        # refresh canvas
        canv.draw()
    def plotAppend(self, data):
        # create an axis
        ax = self.td_figure.add_subplot(111)
        # plot data
        ax.plot(data)
        # refresh canvas
        self.canvas.draw()
    def plotTriple(self, fig, canv, dat1,dat2,dat3, x=None):
        ax1 = fig.add_subplot(311)        
        # discards the old graph
        ax1.clear()
        
        # plot data
        if(x is not None):
            ax1.plot(x,dat1)
        else:
            ax1.plot(dat1)
        ax2 = fig.add_subplot(312,sharex=ax1)
        if(x is not None):
            ax2.plot(x,dat2)
        else:
            ax2.plot(dat2)
        ax3 = fig.add_subplot(313,sharex=ax1)
        if(x is not None):
            ax3.plot(x,dat3)
        else:
            ax3.plot(dat3)
            
        # refresh canvas
        canv.draw()
    def plotTriple_sy(self,fig, canv, dat1, dat2, dat3, x=None):
        ax1 = fig.add_subplot(311)        
        # discards the old graph
        ax1.clear()
        
        # plot data
        print [len(x),len(dat1)]
        if(x is not None):
            ax1.semilogy(x,dat1)
        else:
            ax1.semilogy(dat1)
        ax2 = fig.add_subplot(312,sharex=ax1)
        if(x is not None):
            ax2.semilogy(x,dat2)
        else:
            ax2.semilogy(dat2)
        ax3 = fig.add_subplot(313,sharex=ax1)
        if(x is not None):
            ax3.semilogy(x,dat3)
        else:
            ax3.semilogy(dat3)
            
        # refresh canvas
        canv.draw()
        
        ax1.grid()
        ax2.grid()
        ax3.grid()
        
        return ax1, ax2, ax3
        
    def fft(self,datX,datY):
        rangeX=max(datX) - min(datX)
        ft = np.fft.fft(datY)
        return {'f' : [i/rangeX for i in range(1,len(datX)+1)[::-1]], 'y' : ft[::-1]}
        
    def generateTimeAxis(self,scanTime):
        return np.linspace(0,scanTime,scanTime*self.sampleRate)
        
    def generateFreqSweep(self,startFreq, stopFreq, scanTime, gain, mode='cont'):
        self.timeAxis = self.generateTimeAxis(scanTime)
        if(mode == 'cont'):
            freq = startFreq + (stopFreq - startFreq)/2/scanTime*self.timeAxis
            return gain*np.sin(2*np.pi*freq*self.timeAxis)
        elif(mode == 'disc'):
            freq = startFreq + (stopFreq - startFreq)/2/scanTime*self.timeAxis
            print "Discreet Scan"
            return gain*np.sin(2*np.pi*freq*self.timeAxis)
        return 'Sweep Mode ERROR'
    
    def generateComb(self, fRep, fStart, numModes, scanTime, mode = 'fixed'):
        self.timeAxis = self.generateTimeAxis(scanTime)
        out = np.array([0.0]*len(self.timeAxis))
        if(mode=='fixed'):
            for n in range(0,numModes):
                out += np.sin(2*np.pi*(fStart + n*fRep)*self.timeAxis)
        elif(mode=='rand'):
            for n in range(0,numModes):
                out += np.sin(2*np.pi*(fStart + n*fRep)*self.timeAxis + np.pi*2*np.random.random())
        else:
            return "Mode Error in generateComb"
        return out/max(np.abs(out))
                
                
        
    def freqScan(self,startFreq, stopFreq, scanTime, gain):
        if(self.ui.radio_discSweep.isChecked()):
            mode = 'disc'
        if(self.ui.radio_contSweep.isChecked()):
            mode = 'cont'
        print mode
        audioSignal = self.generateFreqSweep(startFreq,stopFreq,scanTime,gain,mode=mode)
        #self.plotClear(audioSignal)
        recording = self.playRec(audioSignal)
        #self.plotAppend(recording)     
        
        return recording, audioSignal
    
    def playRec(self,audioSig):
        rec = sd.playrec(audioSig,samplerate=self.sampleRate, channels = 2)
        sd.wait()
        return rec
        
    def waveletAnalysis(self,t, dat, startFreq, stopFreq, numWavs):
        #sweep = self.generateFreqSweep(startFreq,stopFreq,len(dat)/self.sampleRate,1.0)
        fOut, rOut = [], []
        for i in range(1,numWavs+1):
            f0 = startFreq + i*(stopFreq-startFreq)/ (numWavs+1)
            t0 = len(dat)/self.sampleRate*(f0- startFreq)/(stopFreq-startFreq)
            envWidth = float(len(dat)/self.sampleRate)/numWavs
            env_func = np.exp(-((t-t0)/2/envWidth)**2)
            sinComp = np.trapz(np.sin(2*np.pi*t*f0)*env_func*dat)
            cosComp = np.trapz(np.cos(2*np.pi*t*f0)*env_func*dat)
            fOut.append(f0); rOut.append(np.sqrt(sinComp**2 + cosComp**2));
            self.ui.fa_progressBar.setValue(int(i/float(numWavs)*100))
        return [fOut, rOut]
        
        
#----------------------Action Methods, No arguments-----------------------
    def scan(self):
        self.lastParam_startFreq = self.ui.startFreq_box.value()
        self.lastParam_stopFreq  = self.ui.stopFreq_box.value()
        self.lastParam_scanTime  = self.ui.scanTime_box.value()
        self.lastParam_gain      = self.ui.gainSlider.value()*.01
        
        if(self.ui.radio_sweepScan.isChecked()):
            self.recording, self.audioSignal = self.freqScan(self.lastParam_startFreq, self.lastParam_stopFreq, self.lastParam_scanTime, self.lastParam_gain)
            print "cont scan"
        elif(self.ui.radio_combScan.isChecked()):
            self.combScan()
            print "comb scan"
        else:
            print "Radio Button Error?"
          
        self.plotTriple(self.td_figure,self.td_canvas,self.audioSignal,self.recording[:,0]/max(self.recording[:,0]),self.recording[:,1]/max(self.recording[:,1]),x=np.linspace(self.lastParam_startFreq,self.lastParam_stopFreq,len(self.audioSignal)))
        
        self.ui.numWavelets_box.setMaximum(len(self.recording))
        
    def plotFreqAnalysis(self):
        scanTime = len(self.audioSignal)/self.sampleRate
        if(self.ui.analysisMethod_box.currentText() == 'Wavelet'):
            wa_a = self.waveletAnalysis(np.linspace(0,scanTime,len(self.recording)), self.audioSignal, self.lastParam_startFreq, self.lastParam_stopFreq, self.ui.numWavelets_box.value())
            wa_r1 = self.waveletAnalysis(np.linspace(0,scanTime,len(self.recording)), self.recording[:,0], self.lastParam_startFreq, self.lastParam_stopFreq, self.ui.numWavelets_box.value())        
            wa_r2 = self.waveletAnalysis(np.linspace(0,scanTime,len(self.recording)), self.recording[:,1], self.lastParam_startFreq, self.lastParam_stopFreq, self.ui.numWavelets_box.value())        
        
            ax1,ax2,ax3 = self.plotTriple_sy(self.fa_figure, self.fa_canvas, wa_a[1]/max(wa_a[1]), wa_r1[1]/max(wa_r1[1]), wa_r2[1]/max(wa_r2[1]), x=wa_a[0])
            ax1.set_xlim(self.lastParam_startFreq, self.lastParam_stopFreq)
            self.fa_canvas.draw()
            
        if(self.ui.analysisMethod_box.currentText() == 'FFT'):
            ft_a  = self.fft(self.timeAxis, self.audioSignal)
            ft_r1 = self.fft(self.timeAxis, self.recording[:,0])
            ft_r2 = self.fft(self.timeAxis, self.recording[:,1])
            
            a_a, a_r1, a_r2 = np.abs(ft_a['y']), np.abs(ft_r1['y']), np.abs(ft_r2['y'])
            
            print len(ft_a['f'])
            print len(a_a)
            
            ax1,ax2,ax3 = self.plotTriple_sy(self.fa_figure, self.fa_canvas, a_a/max(a_a), a_r1/max(a_r1), a_r2/max(a_r2), x=ft_a['f'])
            
            #print [a_a/max(a_a), a_r1/max(a_r1), a_r2/max(a_r2), ft_a['f']]
            
            ax1.set_xlim(self.lastParam_startFreq, self.lastParam_stopFreq)
            self.fa_canvas.draw()
        
    def updateCombStatusText(self):
        lowFreq = min(self.ui.startFreq_box.value(),self.ui.stopFreq_box.value())
        highFreq = max(self.ui.startFreq_box.value(),self.ui.stopFreq_box.value())
        numModes = self.ui.combNumModes_box.value()
        scanCycles = self.ui.combNumCycles_box.value()
        f_rep = float(highFreq-lowFreq)/(numModes-1)
                
        self.ui.combStatusBox.setText('Length of scan (s):\t' + str(float(scanCycles)/f_rep) + '\n' + 
                                        'Repetition Freq (Hz):\t' + str(f_rep))
                                        
    def combScan(self):
        self.lastParam_startFreq = self.ui.startFreq_box.value()
        self.lastParam_stopFreq  = self.ui.stopFreq_box.value()
        self.lastParam_scanTime  = self.ui.scanTime_box.value()
        self.lastParam_gain      = self.ui.gainSlider.value()*.01
        
        lowFreq = min(self.ui.startFreq_box.value(),self.ui.stopFreq_box.value())
        highFreq = max(self.ui.startFreq_box.value(),self.ui.stopFreq_box.value())
        numModes = self.ui.combNumModes_box.value()
        scanCycles = self.ui.combNumCycles_box.value()
        f_rep = float(highFreq-lowFreq)/(numModes-1)
        
        self.audioSignal = self.lastParam_gain * self.generateComb(f_rep,lowFreq,numModes,float(scanCycles)/f_rep, mode = 'rand')
        self.recording = self.playRec(self.audioSignal)
        
        print 'asdf'+str(len(self.audioSignal))
        print 'asdf'+str(len(self.recording))
        
    def saveData(self):        
        fileName = QtGui.QFileDialog.getSaveFileName(self, 'Save Data as', os.getcwd())#, selectedFilter='*.fscn')
        if fileName:
            fHandle = open(fileName,'w')
            pickle.dump({'t' : self.timeAxis, 'signal' : self.audioSignal, 'r1' : self.recording[:,0], 'r2' : self.recording[:,1]}, fHandle)
            fHandle.close()
            
    def loadData(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, 'Save Data as', os.getcwd())
        if(fileName):
            fHandle = open(fileName)
            ld = pickle.load(fHandle)
            self.timeAxis, self.audioSignal, self.recording = ld['t'], ld['signal'], np.array(zip(ld['r1'],ld['r2']))
            self.plotTriple(self.td_figure, self.td_canvas, self.audioSignal, self.recording[:,0], self.recording[:,1])
 
if __name__ == "__main__":
        app = QtGui.QApplication(sys.argv)
        myapp = MyDialog()
        myapp.show()
        sys.exit(app.exec_())