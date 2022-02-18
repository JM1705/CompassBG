import setup
from os import getenv

appdata = getenv('LOCALAPPDATA') + '\CompassBG'
setup.cfgCreate(appdata)