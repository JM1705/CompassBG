import compass
import setup
from json import load
from datetime import datetime
from ctypes import windll
from os import listdir, getenv, path
from random import randint
from PIL import Image, ImageDraw, ImageFont, ImageOps
from requests import get
from re import search

version = '2.3.1'
print('CompassBG | Version: '+str(version)+'\n')

# Create configuration file if it doesn't exist yet
appdata = getenv('LOCALAPPDATA') + '\CompassBG'
if not path.exists(appdata+'\cfg.json'):
    setup.cfgCreate(appdata)

# Get information from cfg file
try:
    with open(appdata + '\cfg.json', 'r') as f:
        cfg = load(f)
        pwd = cfg['password']
        unm = cfg['username']
        bgpath = cfg['background_path']
        size = cfg['screen_resolution']
        fontsize = cfg['font_size']
        linespace = cfg['line_spacing']
        startpos = cfg['start_position']
        textcolour = cfg['text_colour']
        fontfile = cfg['font_file']
        highcontrast = cfg['high_contrast']
except:
    raise KeyError('Config file corrupt or outdated, please run ClearData and then run CompassBG again')

# Get time information
now = datetime.now()
todayDate = now.strftime("%Y-%m-%d")
print(todayDate)

# Wait for internet connection
print("Waiting for internet connection.")
connected = False
while not connected:
    try:
        request = get('https://www.google.com', timeout=1)
        print("Connected to the internet")
        connected = True
    except:
        pass


# Get data from Compass
print('Getting calender data from Compass')
try:
    c = compass.CompassAPI(unm, pwd)
except KeyError:
    raise ValueError('Password and username are incorrect, or the config file is corrupt fix the cfg.json file in appdata or run ClearData and then run CompassBG.')
except:
    raise ValueError('Compass threw an error, idk what happened lol, try again?')
    quit()
events = c.get_calender_events_by_user(todayDate)
lessons = []
for i in events:
    eventInfo = i['longTitleWithoutTime'].split(' - ')
    lessons.append(eventInfo)
lessons = sorted(lessons)


# Fix strikethrough
k = []
for i in lessons:
    l = []
    for j in i:
        if 'strike' in j:
            strike = '<strike>(.*?)</strike>&nbsp;'
            strikeStr = search(strike, j).group(1)
            striked = strikeStr + ' (substituted by'
            replaceStr = '<strike>'+strikeStr+'</strike>&nbsp;'
            j = j.replace(replaceStr, striked) + ')'
        l.append(j)
    k.append(l)
lessons = k
    

# Create text for background editing
print('Creating text for editing background')
editText = [todayDate+': ']
for i in lessons:
    tempstr = ''
    if len(i) == 3:
        tempstr = '[?] - '+i[0]+' - '+i[1]+' - '+i[2]
    else:
        tempstr += '['+i[0]+']'
        for j in range(len(i)-1):
            tempstr += ' - '+i[j+1]
    print(tempstr)
    editText.append(tempstr)

# Select background from folder
print('Selecting background')
bgs = []
for file in listdir(bgpath):
    bgs.append(file)
sbgpath = bgpath+"\\"+bgs[randint(0, len(bgs)-1)]

# Edit and save background image
print('Editing background image with text')
if highcontrast:
    # Create alpha channel of text
    textalpha = Image.new('L', size)
    draw = ImageDraw.Draw(textalpha)
    font = ImageFont.truetype(fontfile, fontsize)
    for i in range(len(editText)):
        pos = startpos[0], startpos[1] +linespace * i
        draw.text(pos, editText[i], 255, font=font)

    # Create negative of wallpaper    
    img = Image.open(sbgpath)
    img = img.resize(size, Image.ANTIALIAS)
    negimg = ImageOps.invert(img)
    negimg.putalpha(textalpha)
    
    # Overlay negative on original with alpha channel of text
    img = img.convert("RGBA")
    negimg = negimg.convert("RGBA")
    img = Image.alpha_composite(img, negimg)
    img.save(appdata+r'\tempbg.png')
    
else:
    img = Image.open(sbgpath)
    img = img.resize(size, Image.ANTIALIAS)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(fontfile, fontsize)
    for i in range(len(editText)):
        pos = startpos[0], startpos[1] +linespace * i
        draw.text(pos, editText[i], tuple(textcolour), font=font)
    img.save(appdata+r'\tempbg.png')

# Set edited image as background
print('Setting image as background')
windll.user32.SystemParametersInfoW(20, 0, appdata+r'\tempbg.png', 0)

print('Success')