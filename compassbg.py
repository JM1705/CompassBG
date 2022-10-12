import compass
import setup
from json import load, dump
from random import randint
from os import listdir, getenv, path
from ctypes import windll
from screeninfo import get_monitors


# Start of code
version = '2.5.2'
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
        fontsize = cfg['font_size']
        linespace = cfg['line_spacing']
        startpos = cfg['start_position']
        textcolour = cfg['text_colour']
        fontfile = cfg['font_file']
        highcontrast = cfg['high_contrast']
        try:
            titlemod = cfg['title_size_modifier']
        except:
            with open(appdata + '\cfg.json', 'w') as g:
                cfg['title_size_modifier'] = 8
                titlemod = 8
                dump(cfg, g, indent = '\t')
        try:
            titleSpace = cfg['title_spacing']
        except:
            with open(appdata + '\cfg.json', 'w') as g:
                cfg['title_spacing'] = 2
                titlespace = 2
                dump(cfg, g, indent = '\t')
        try:
            maxTries = cfg['max_tries']
        except:
            with open(appdata + '\cfg.json', 'w') as g:
                cfg['max_tries'] = 3
                maxTries = 3
                dump(cfg, g, indent = '\t')
except:
    raise KeyError('Config file corrupt or outdated, please run ClearData and then run CompassBG again')

# Finding Screen resolution
monitors = get_monitors()
size = [monitors[0].width, monitors[0].height]

# Select background from folder
print('Selecting background')
if path.isfile(bgpath):
    sbgpath = bgpath
else:
    bgs = []
    for file in listdir(bgpath):
        bgs.append(file)
    sbgpath = bgpath+"\\"+bgs[randint(0, len(bgs)-1)]


# Set temporary image as background
print('Setting temporary image as background')
windll.user32.SystemParametersInfoW(20, 0, sbgpath, 0)


# Importing more liblaries
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps
from requests import get
from re import search


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
compTries = 0
maxTries
compSuccess = False
while compSuccess == False:
    try:
        c = compass.CompassAPI(unm, pwd)
    except KeyError:
        raise ValueError('Password and username are incorrect, or the config file is corrupt fix the cfg.json file in appdata or run ClearData and then run CompassBG.')
        quit()
    except:
        compTries += 1
        print('Could not get data from Compass. Tries left: '+str(maxTries-compTries))
    else:
        compSuccess = True
    if compTries > maxTries:
        raise ValueError('Compass returned more than '+str(maxTries)+' errors, exiting')
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
editText = []
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

daysInWeek = ['Mon', 'Tues', 'Wednes', 'Thurs', 'Fri', 'Satur', 'Sun']
titleText = todayDate+'    '+daysInWeek[datetime.today().weekday()]+'day: '

# Edit and save background image
print('Editing background image with text')
if highcontrast:
    # High contrast text
    # Create alpha channel of text
    textalpha = Image.new('L', size)
    draw = ImageDraw.Draw(textalpha)
    font = ImageFont.truetype(fontfile, fontsize)
    titleFont = ImageFont.truetype(fontfile, fontsize+titlemod)
    draw.text((startpos[0], startpos[1]), titleText, 255, font=titleFont)
    for i in range(len(editText)):
        pos = startpos[0], startpos[1] +linespace * (i+1)+titlemod+titleSpace
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
    # Coloured text
    img = Image.open(sbgpath)
    img = img.resize(size, Image.ANTIALIAS)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(fontfile, fontsize)
    titleFont = ImageFont.truetype(fontfile, fontsize+titlemod)
    draw.text((startpos[0], startpos[1]), titleText, tuple(textcolour), font=titleFont)
    for i in range(len(editText)):
        pos = startpos[0], startpos[1] +linespace * (i+1)+titlemod+titleSpace
        draw.text(pos, editText[i], tuple(textcolour), font=font)
    img.save(appdata+r'\tempbg.png')


# Set edited image as background
print('Setting image as background')
windll.user32.SystemParametersInfoW(20, 0, appdata+r'\tempbg.png', 0)
print('Success')