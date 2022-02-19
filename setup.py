import json
from getpass import getpass
import os
import sys
import winshell
from win32com.client import Dispatch
from msvcrt import getch
import stdiomask

startup = winshell.startup()

def ynbool(string):
    if string == 'y':
        return True
    else:
        return False

def cfgCreate(path):
    cfgpath = path + '\cfg.json'
    isExe = False
    if getattr(sys, 'frozen', False):
        isExe = True
        application_path = os.path.dirname(sys.executable)
        
    startPath = winshell.startup() + r'\compassbgw.lnk'
    
    print("Welcome to the CompassBG setup assistant")
    print("More advanced settings can be accessed by opening the configuration file in Appdata")
    input("Press Enter to start")
    
    bgpath = input("Full background folder path (string): ")
    size = int(input("Horizontal resolution (int):")), int(input("Vertical resolution (int): "))
    highcontrast = ynbool(input("Make font high contrast? (y/n) "))
    autorun = ynbool(input("Run this script on startup? (Only works with .exe version) (y/n): "))
    unm = input("Username for Compass (string): ")
    pwd = stdiomask.getpass(prompt= "Password for Compass (string): ", mask='*')
    
    fontsize = 16
    linespace = 20
    startpos = [10, 10]
    textcolor = [255, 255, 255]
    fontfile = "C:\\Windows\\Fonts\\calibrib.ttf"
    
    if not os.path.exists(path):
        os.makedirs(path)

    if not os.path.exists(cfgpath):
        open(cfgpath, 'a').close()
    
    with open(cfgpath, 'w') as f:
        cfg = {}
        cfg['username'] = unm
        cfg['password'] = pwd
        cfg['background_path'] = bgpath
        cfg['screen_resolution'] = size
        cfg['font_size'] = fontsize
        cfg['font_file'] = fontfile
        cfg['line_spacing'] = linespace
        cfg['start_position'] = startpos
        cfg['text_colour'] = textcolor
        cfg['run_on_startup'] = autorun
        cfg['high_contrast'] = highcontrast
        json.dump(cfg, f, indent = '\t')
        
    if autorun == True and isExe:
        target = application_path + r'\compassbgw.exe'
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(startPath)
        shortcut.Targetpath = target
        shortcut.save()
    else:
        if os.path.exists(startPath):
            os.remove(startPath)