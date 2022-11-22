# Main CompassBG script
import compass
from json import load, dump
from random import randint
from os import listdir, getenv, path
from ctypes import windll
from screeninfo import get_monitors
import compassBGQT as CBSettings
from types import SimpleNamespace
from fileCodeTranslate import translateDict


# Start of code
version = '2.7.0'
print('CompassBG | Version: '+str(version)+'\n')


# Create configuration file if it doesn't exist yet
appdata = getenv('LOCALAPPDATA') + '\CompassBG'
cfgLoc = appdata + "\cfg.json"
if not path.exists(appdata+'\cfg.json'):
    CBSettings.runSettings(appdata)

# Get information from cfg file

# Load config file as dictionary
tempCfg = load(open(cfgLoc, 'r'))

# Change the names of keys so the code doesn't break
tempCfg = translateDict(tempCfg, "code")

# Convert dictionary to namespace 
cfg = SimpleNamespace(**tempCfg)

# Finding Screen resolution
monitors = get_monitors()
size = [monitors[0].width, monitors[0].height]

# Select background from folder
print('Selecting background')
if path.isfile(cfg.bgpath):
    sbgpath = cfg.bgpath
else:
    bgs = []
    for file in listdir(cfg.bgpath):
        bgs.append(file)
    sbgpath = cfg.bgpath+"\\"+bgs[randint(0, len(bgs)-1)]


# Set temporary image as background
print('Setting temporary image as background')
windll.user32.SystemParametersInfoW(20, 0, sbgpath, 0)


# Importing more liblaries
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
from requests import get
from re import search
from dateutil import tz, parser
    
# Defining function    
def compassTimeTo24h(timeStr):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = parser.parse(timeStr.replace('Z', ''))
    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    return central.strftime('%H:%M')


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
compSuccess = False
while compSuccess == False:
    try:
        c = compass.CompassAPI(cfg.unm, cfg.pwd)
    except KeyError:
        raise ValueError('Password and username are incorrect, or the config file is corrupt fix the cfg.json file in appdata or run ClearData and then run CompassBG.')
        quit()
    except:
        compTries += 1
        print('Could not get data from Compass. Tries left: '+str(cfg.maxTries-compTries))
    else:
        compSuccess = True
    if compTries > cfg.maxTries:
        raise ValueError('Compass returned more than '+str(cfg.maxTries)+' errors, exiting')
events = c.get_calender_events_by_user(todayDate)

lessons = []
lessonTimes = []
for i in events:
    eventInfo = i['longTitleWithoutTime'].split(' - ')
    lessons.append(eventInfo)
    times = []
    times.append(compassTimeTo24h(i['start']))
    times.append(compassTimeTo24h(i['finish']))
    lessonTimes.append(times)
# lessons = sorted(lessons)


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
for inum in range(len(lessons)):
    i = lessons[inum]
    t = lessonTimes[inum]
    # This is a temporary timestamp for sorting
    tempstr = t[0]+'-'+t[1]
    if len(i) == 3:
        tempstr +='[?] '+' - '+i[0]+' - '+i[1]+' - '+i[2]
    else:
        tempstr += '['+i[0]+']'
        for j in range(len(i)-1):
            tempstr += ' - '+i[j+1]
    print(tempstr)
    editText.append(tempstr)
editText = sorted(editText)
editTimes = []
for i in lessonTimes:
    editTimes.append(i[0]+'-'+i[1])
editTimes = sorted(editTimes)

# Remove temporary timestamp from editText
for i in range(len(editText)):
    editText[i] = editText[i].replace(editTimes[i], '')


daysInWeek = ['Mon', 'Tues', 'Wednes', 'Thurs', 'Fri', 'Satur', 'Sun']
titleText = todayDate+'    '+daysInWeek[datetime.today().weekday()]+'day: '

# Edit and save background image
print('Editing background image with text')
if cfg.highcontrast:
    # High contrast text
    # Create alpha channel of text
    textalpha = Image.new('L', size)
    draw = ImageDraw.Draw(textalpha)
    font = ImageFont.truetype(cfg.fontfile, cfg.fontsize)
    titleFont = ImageFont.truetype(cfg.fontfile, cfg.fontsize+cfg.titlemod)
    draw.text((cfg.startpos[0], cfg.startpos[1]), titleText, 255, font=titleFont)
    
    for i in range(len(editTimes)):
        pos = cfg.startpos[0], cfg.startpos[1] +cfg.linespace * (i+1)+cfg.titlemod+cfg.titlespace
        draw.text(pos, editTimes[i], 255, font=font)

    for i in range(len(editText)):
        pos = cfg.startpos[0]+9*cfg.fontsize+10, cfg.startpos[1] +cfg.linespace * (i+1)+cfg.titlemod+cfg.titlespace
        draw.text(pos, editText[i], 255, font=font)

    # Create negative of wallpaper    
    img = Image.open(sbgpath)
    img = img.resize(size, Image.Resampling.LANCZOS)
    negimg = ImageOps.invert(img)
    negimg = negimg.filter(ImageFilter.BoxBlur(12))
    negimg.putalpha(textalpha)
    
    # Overlay negative on original with alpha channel of text
    img = img.convert("RGBA")
    negimg = negimg.convert("RGBA")
    img = Image.alpha_composite(img, negimg)
    img.save(appdata+r'\tempbg.png')
    
else:
    # Coloured text
    img = Image.open(sbgpath)
    img = img.resize(size, Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(cfg.fontfile, cfg.fontsize)
    titleFont = ImageFont.truetype(cfg.fontfile, cfg.fontsize+cfg.titlemod)
    draw.text((cfg.startpos[0], cfg.startpos[1]), titleText, tuple(cfg.textcolour), font=titleFont)
    
    for i in range(len(editTimes)):
        pos = cfg.startpos[0], cfg.startpos[1] +cfg.linespace * (i+1)+cfg.titlemod+cfg.titlespace
        draw.text(pos, editTimes[i], tuple(cfg.textcolour), font=font)

    for i in range(len(editText)):
        pos = cfg.startpos[0]+11*cfg.fontsize/1.7+10, cfg.startpos[1] +cfg.linespace * (i+1)+cfg.titlemod+cfg.titlespace
        draw.text(pos, editText[i], tuple(cfg.textcolour), font=font)

    img.save(appdata+r'\tempbg.png')


# Set edited image as background
print('Setting image as background')
windll.user32.SystemParametersInfoW(20, 0, appdata+r'\tempbg.png', 0)
print('Success')