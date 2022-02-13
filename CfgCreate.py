import json

print("Create the cfg.json file for the Compass background python script")
input("Press Enter to start")

bgpath = input("Full background folder path (string):")
size = int(input("Horizontal resolution (int):")), int(input("Vertical resolution (int):"))
sendnotif = bool(input("notification every time code is run (bool):"))
unm = input("Username for Compass (string):")
pwd = input("Password for Compass (string):")

fontsize = 16
linespace = 20
startpos = [10, 10]
textcolor = [255, 255, 255]
fontfile = 'Roboto-Medium.ttf'

with open('cfg.json', 'w') as f:
    cfg = {}
    cfg['username'] = unm
    cfg['password'] = pwd
    cfg['background_path'] = bgpath
    cfg['screen_resolution'] = size
    cfg['font_size'] = fontsize
    cfg['font_file'] = fontfile
    cfg['line_spacing'] = linespace
    cfg['start_position'] = startpos
    cfg['send_notification'] = sendnotif
    cfg['text_colour'] = textcolor
    json.dump(cfg, f, indent = '\t')