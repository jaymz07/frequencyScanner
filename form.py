# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(507, 538)
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(0, 50, 501, 481))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.settings_tab = QtGui.QWidget()
        self.settings_tab.setObjectName(_fromUtf8("settings_tab"))
        self.formLayoutWidget = QtGui.QWidget(self.settings_tab)
        self.formLayoutWidget.setGeometry(QtCore.QRect(80, 90, 271, 131))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.startFreq_box = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.startFreq_box.setMinimum(10.0)
        self.startFreq_box.setMaximum(19999.99)
        self.startFreq_box.setProperty("value", 1000.0)
        self.startFreq_box.setObjectName(_fromUtf8("startFreq_box"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.startFreq_box)
        self.stopFreq_box = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.stopFreq_box.setMinimum(10.0)
        self.stopFreq_box.setMaximum(20000.0)
        self.stopFreq_box.setProperty("value", 22.0)
        self.stopFreq_box.setObjectName(_fromUtf8("stopFreq_box"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.stopFreq_box)
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.scanTime_box = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.scanTime_box.setMinimum(0.01)
        self.scanTime_box.setProperty("value", 3.0)
        self.scanTime_box.setObjectName(_fromUtf8("scanTime_box"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.scanTime_box)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtGui.QLabel(self.settings_tab)
        self.label_4.setGeometry(QtCore.QRect(100, 20, 191, 41))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayoutWidget = QtGui.QWidget(self.settings_tab)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(300, 260, 160, 121))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gainSlider = QtGui.QSlider(self.gridLayoutWidget)
        self.gainSlider.setMaximum(100)
        self.gainSlider.setProperty("value", 50)
        self.gainSlider.setOrientation(QtCore.Qt.Vertical)
        self.gainSlider.setObjectName(_fromUtf8("gainSlider"))
        self.gridLayout.addWidget(self.gainSlider, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 1, 1, 1)
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.settings_tab)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(30, 260, 231, 141))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkBox_audioOutEnabled = QtGui.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox_audioOutEnabled.setObjectName(_fromUtf8("checkBox_audioOutEnabled"))
        self.verticalLayout.addWidget(self.checkBox_audioOutEnabled)
        self.tabWidget.addTab(self.settings_tab, _fromUtf8(""))
        self.plot_tab = QtGui.QWidget()
        self.plot_tab.setObjectName(_fromUtf8("plot_tab"))
        self.verticalLayoutWidget = QtGui.QWidget(self.plot_tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 481, 431))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.plot_layout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.plot_layout.setObjectName(_fromUtf8("plot_layout"))
        self.tabWidget.addTab(self.plot_tab, _fromUtf8(""))
        self.scanButton = QtGui.QPushButton(Dialog)
        self.scanButton.setGeometry(QtCore.QRect(390, 20, 99, 27))
        self.scanButton.setObjectName(_fromUtf8("scanButton"))

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Start Freq (Hz)", None))
        self.label_2.setText(_translate("Dialog", "Stop Freq (Hz)", None))
        self.label_3.setText(_translate("Dialog", "Scan Time (sec)", None))
        self.label_4.setText(_translate("Dialog", "Scan Settings", None))
        self.label_5.setText(_translate("Dialog", "Gain", None))
        self.checkBox_audioOutEnabled.setText(_translate("Dialog", "Audio Out Enabled", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings_tab), _translate("Dialog", "Settings", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plot_tab), _translate("Dialog", "Plot", None))
        self.scanButton.setText(_translate("Dialog", "Scan", None))

