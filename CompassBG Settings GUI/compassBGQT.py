import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from os import getenv, path
from json import load, dump


def loadDefaults():
    global pwd, unm, bgpath, fontsize, linespace, autorun, startpos, fontfile, textcolour, highcontrast, titlemod, titlespace, maxTries
    with open('defaultCfg.json', 'r') as f:
        cfg = load(f)
        pwd = cfg['password']
        unm = cfg['username']
        bgpath = cfg['background_path']
        fontsize = cfg['font_size']
        linespace = cfg['line_spacing']
        autorun = cfg['run_on_startup']
        startpos = cfg['start_position']
        textcolour = cfg['text_colour']
        fontfile = cfg['font_file']
        highcontrast = cfg['high_contrast']
        titlemod = cfg['title_size_modifier']
        titlespace = cfg['title_spacing']
        maxTries = cfg['max_tries']
    refreshValues()
    print('Defaults loaded')


def refreshValues():
    global window
    self = window
    try:
        self.findChild(QLineEdit, 'LEUnm').setText(unm)
        self.findChild(QLineEdit, 'LEPwd').setText(pwd)
        self.findChild(QLineEdit, 'LETxtCol').setText('%02x%02x%02x' % tuple(textcolour))
        self.findChild(QSpinBox, 'SBFontSize').setValue(fontsize)
        self.findChild(QSpinBox, 'SBLineSpace').setValue(linespace)
        self.findChild(QSpinBox, 'SBStartX').setValue(startpos[0])
        self.findChild(QSpinBox, 'SBStartY').setValue(startpos[1])
        self.findChild(QSpinBox, 'SBTitleMod').setValue(titlemod)
        self.findChild(QSpinBox, 'SBTitleSpace').setValue(titlespace)
        self.findChild(QCheckBox, 'CBContrast').setChecked(highcontrast)
        self.findChild(QCheckBox, 'CBStartup').setChecked(autorun)
        self.findChild(QSpinBox, 'SBMaxTries').setValue(maxTries)
    except:
        loadDefaults()
        self.findChild(QLineEdit, 'LEUnm').setText(unm)
        self.findChild(QLineEdit, 'LEPwd').setText(pwd)
        self.findChild(QLineEdit, 'LETxtCol').setText('%02x%02x%02x' % tuple(textcolour))
        self.findChild(QSpinBox, 'SBFontSize').setValue(fontsize)
        self.findChild(QSpinBox, 'SBLineSpace').setValue(linespace)
        self.findChild(QSpinBox, 'SBStartX').setValue(startpos[0])
        self.findChild(QSpinBox, 'SBStartY').setValue(startpos[1])
        self.findChild(QSpinBox, 'SBTitleMod').setValue(titlemod)
        self.findChild(QSpinBox, 'SBTitleSpace').setValue(titlespace)
        self.findChild(QCheckBox, 'CBContrast').setChecked(highcontrast)
        self.findChild(QCheckBox, 'CBStartup').setChecked(autorun)
        self.findChild(QSpinBox, 'SBMaxTries').setValue(maxTries)


def BGDirSelect():
    global bgpath
    bgpath=QFileDialog.getExistingDirectory()
    print(bgpath)
    

def FontSelect():
    global fontfile
    title = "Select Font"
    qfd = QFileDialog()
    path = "."
    filter = "ttf(*.ttf)"
    fontfile=QFileDialog.getOpenFileName(qfd, title, path, filter)[0]
    print(fontfile)


def Apply():
    global bgpath, fontfile, window

    self = window
    unm = self.findChild(QLineEdit, 'LEUnm').text()
    pwd = self.findChild(QLineEdit, 'LEPwd').text()
    hextextcol = self.findChild(QLineEdit, 'LETxtCol').text()
    lv = len(hextextcol)
    textcolour = tuple(int(hextextcol[i:i+lv//3], 16) for i in range(0, lv, lv//3))
    fontsize = self.findChild(QSpinBox, 'SBFontSize').value()
    linespace = self.findChild(QSpinBox, 'SBLineSpace').value()
    x=self.findChild(QSpinBox, 'SBStartX').value()
    y=self.findChild(QSpinBox, 'SBStartY').value()
    startpos = [x, y]
    titlemod = self.findChild(QSpinBox, 'SBTitleMod').value()
    titlespace = self.findChild(QSpinBox, 'SBTitleSpace').value()
    highcontrast = self.findChild(QCheckBox, 'CBContrast').isChecked()
    autorun = self.findChild(QCheckBox, 'CBStartup').isChecked()
    maxTries = self.findChild(QSpinBox, 'SBMaxTries').value()

    with open(cfgLoc, 'w') as f:
        saveCfg = {}
        saveCfg['username'] = unm
        saveCfg['password'] = pwd
        saveCfg['background_path'] = bgpath
        saveCfg['font_size'] = fontsize
        saveCfg['font_file'] = fontfile
        saveCfg['line_spacing'] = linespace
        saveCfg['start_position'] = startpos
        saveCfg['text_colour'] = textcolour
        saveCfg['run_on_startup'] = autorun
        saveCfg['high_contrast'] = highcontrast
        saveCfg['title_size_modifier'] = titlemod
        saveCfg['title_spacing'] = titlespace
        saveCfg['max_tries'] = maxTries
        dump(saveCfg, f, indent = '\t')
    print('Saved to cfg.json')



class Ui(QMainWindow):
    def __init__(self):
        global bgButton
        
        super(Ui, self).__init__()
        uic.loadUi('lightSettings.ui', self)

        self.findChild(QPushButton, 'BrowseBG').clicked.connect(BGDirSelect)
        self.findChild(QPushButton, 'BrowseFont').clicked.connect(FontSelect)
        self.findChild(QPushButton, 'BApply').clicked.connect(Apply)
        self.findChild(QPushButton, 'BDefault').clicked.connect(loadDefaults)

        self.show()


def startWindow():
    global pwd, unm, bgpath, fontsize, linespace, autorun, startpos, fontfile, textcolour, highcontrast, titlemod, titlespace, maxTries, window, appdata, bgButton, fontButton, cfgLoc
    app = QApplication(sys.argv)
    window = Ui()


    bgpath = ""
    bgButton = []
    fontfile = ""
    fontButton = []
    cfgLoc = appdata = getenv('LOCALAPPDATA') + '\CompassBG\cfg.json'


    try:
        if path.exists(cfgLoc):
            with open(cfgLoc, 'r') as f:
                cfg = load(f)
                pwd = cfg['password']
                unm = cfg['username']
                bgpath = cfg['background_path']
                fontsize = cfg['font_size']
                linespace = cfg['line_spacing']
                autorun = cfg['run_on_startup']
                startpos = cfg['start_position']
                textcolour = cfg['text_colour']
                fontfile = cfg['font_file']
                highcontrast = cfg['high_contrast']
                titlemod = cfg['title_size_modifier']
                titlespace = cfg['title_spacing']
                maxTries = cfg['max_tries']
        else:
            loadDefaults()
    except:
        loadDefaults()

    refreshValues()

    app.exec_()