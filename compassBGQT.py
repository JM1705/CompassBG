# Script for displaying settings GUI, run by compassbg.py
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from os import path, makedirs
from json import load, dump
from pathlib import Path
from types import SimpleNamespace    
from fileCodeTranslate import translateDict

class runSettings:
    def __init__(self, appdata):
        app = QApplication(sys.argv)
        self.ui = QMainWindow()
        uic.loadUi('lightSettings.ui', self.ui)

        # Connect buttons to functions
        self.ui.findChild(QPushButton, 'BrowseBG').clicked.connect(self.BGDirSelect)
        self.ui.findChild(QPushButton, 'BrowseFont').clicked.connect(self.FontSelect)
        self.ui.findChild(QPushButton, 'BApply').clicked.connect(self.Apply)
        self.ui.findChild(QPushButton, 'BDefault').clicked.connect(self.loadDefaults)

        # Appdata including compassBG subfolder
        self.appdata = appdata
        self.cfgLoc = self.appdata + "\cfg.json"

        # Load settings or current
        if path.exists(self.cfgLoc):
            self.loadCurrent()
        else:
            self.loadDefaults()

        # Run app
        self.ui.show()
        app.exec_()


    def loadCurrent(self):
        # Load config file as dictionary
        tempCfg = load(open(self.cfgLoc, 'r'))

        # Change the names of keys so the code doesn't break
        tempCfg = translateDict(tempCfg, "code")

        # Convert dictionary to namespace 
        self.cfg = SimpleNamespace(**tempCfg)
        
        self.refreshValues()
        print("Current settings loaded from: "+self.cfgLoc)


    def loadDefaults(self):
        bgtemppath = str(Path.home() / "Pictures") + "\CompassBG"
        if not path.exists(bgtemppath):
            makedirs(bgtemppath)
            print("Created temporary background images path in: "+bgtemppath)

        # Load config file as dictionary
        tempCfg = load(open('defaultCfg.json', 'r'))
        
        # Change the names of keys so the code doesn't break
        tempCfg = translateDict(tempCfg, "code")

        # Convert dictionary to namespace 
        self.cfg = SimpleNamespace(**tempCfg)

        self.refreshValues()
        print('Defaults loaded')
    
    def refreshValues(self):
        self.ui.findChild(QLineEdit, 'LEUnm').setText(self.cfg.unm)
        self.ui.findChild(QLineEdit, 'LEPwd').setText(self.cfg.pwd)
        self.ui.findChild(QLineEdit, 'LETxtCol').setText('%02x%02x%02x' % tuple(self.cfg.textcolour))
        self.ui.findChild(QSpinBox, 'SBFontSize').setValue(self.cfg.fontsize)
        self.ui.findChild(QSpinBox, 'SBLineSpace').setValue(self.cfg.linespace)
        self.ui.findChild(QSpinBox, 'SBStartX').setValue(self.cfg.startpos[0])
        self.ui.findChild(QSpinBox, 'SBStartY').setValue(self.cfg.startpos[1])
        self.ui.findChild(QSpinBox, 'SBTitleMod').setValue(self.cfg.titlemod)
        self.ui.findChild(QSpinBox, 'SBTitleSpace').setValue(self.cfg.titlespace)
        self.ui.findChild(QCheckBox, 'CBContrast').setChecked(self.cfg.highcontrast)
        self.ui.findChild(QCheckBox, 'CBStartup').setChecked(self.cfg.autorun)
        self.ui.findChild(QSpinBox, 'SBMaxTries').setValue(self.cfg.maxTries)
        print("Refreshed values in UI")


    def BGDirSelect(self):
        self.cfg.bgpath=QFileDialog.getExistingDirectory()
        print("New background path selected: "+self.cfg.bgpath)


    def FontSelect(self):
        # Popup window for selecting font
        title = "Select Font"
        qfd = QFileDialog()
        path = "."
        filter = "ttf(*.ttf)"
        self.cfg.fontfile=QFileDialog.getOpenFileName(qfd, title, path, filter)[0]
        print("New font file selected: "+self.cfg.fontfile)


    def Apply(self):
        # Fetch information from input fields in ui
        self.cfg.unm = self.ui.findChild(QLineEdit, 'LEUnm').text()
        self.cfg.pwd = self.ui.findChild(QLineEdit, 'LEPwd').text()
        self.cfg.fontsize = self.ui.findChild(QSpinBox, 'SBFontSize').value()
        self.cfg.linespace = self.ui.findChild(QSpinBox, 'SBLineSpace').value()
        self.cfg.titlemod = self.ui.findChild(QSpinBox, 'SBTitleMod').value()
        self.cfg.titlespace = self.ui.findChild(QSpinBox, 'SBTitleSpace').value()
        self.cfg.highcontrast = self.ui.findChild(QCheckBox, 'CBContrast').isChecked()
        self.cfg.autorun = self.ui.findChild(QCheckBox, 'CBStartup').isChecked()
        self.cfg.maxTries = self.ui.findChild(QSpinBox, 'SBMaxTries').value()
        
        # Hex text colour to rgb
        hextextcol = self.ui.findChild(QLineEdit, 'LETxtCol').text()
        lv = len(hextextcol)
        self.cfg.textcolour = tuple(int(hextextcol[i:i+lv//3], 16) for i in range(0, lv, lv//3))

        # Combine x and y values of starting position
        x=self.ui.findChild(QSpinBox, 'SBStartX').value()
        y=self.ui.findChild(QSpinBox, 'SBStartY').value()
        self.cfg.startpos = [x, y]

        # Save self.cfg to settings file
        
        # Change the names of keys so the code doesn't break
        tempCfg = translateDict(vars(self.cfg), "file")

        dump(tempCfg, open(self.cfgLoc, 'w'), indent = '\t')
        print('Saved settings to: '+self.cfgLoc)