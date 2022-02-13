import compass
import cbgcfg
from json import load
from datetime import datetime
from ctypes import windll
from os import listdir, getcwd, getenv, path
from random import randint
from PIL import Image, ImageDraw, ImageFont
from requests import get
from re import search

version = '2.1.5'
print('CompassAutoBackground | Version: '+str(version)+'\n')

#Cfg json thing
appdata = getenv('LOCALAPPDATA') + '\CompassBG'
if not path.exists(appdata):
    cbgcfg.cfgCreate(appdata)
    
# Get information from cfg file
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
c = compass.CompassAPI(unm, pwd)
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
img = Image.open(sbgpath)
# long step below
img = img.resize(size, Image.ANTIALIAS)
# long step below
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