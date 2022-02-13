import json
from getpass import getpass
import os

def cfgCreate(path):
    cfgpath = path + '\cfg.json'
    
    print("Welcome to the CompassBG setup assisstant")
    print("More advanced settings can be accessed by opening the configuration file in Appdata")
    input("Press Enter to start")
    
    bgpath = input("Full background folder path (string):")
    size = int(input("Horizontal resolution (int):")), int(input("Vertical resolution (int):"))
    unm = input("Username for Compass (string):")
    pwd = getpass("Password for Compass (string):")
    
    fontsize = 16
    linespace = 20
    startpos = [10, 10]
    textcolor = [255, 255, 255]
    fontfile = "C:\\Windows\\Fonts\\calibrib.ttf"
    
    if not os.path.exists(cfgpath):
        os.makedirs(path)
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
        json.dump(cfg, f, indent = '\t')