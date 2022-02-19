# CompassBG
Create and set a wallpaper with the Compass schedule for the day


## WARNING!!! THIS SCRIPT SAVES YOUR COMPASS LOGIN CREDENTIALS AS PLAIN TEXT IN A JSON CONFIGURATION FILE. DO NOT SHARE THIS FILE.


## Dependencies:

	Windows 10 (11 would probably work as well)


## Instructions:

Step 1:
	Create a directory with wallpaper images

Step 2:
	Place the CompassBG folder in install location
	(The optional startup shortcut generated by the setup assisstant will break if the CompassBG directory is moved)

Step 3:
	Create a configuration file by running compassbg.exe manually
	
	This will create:
	
	1. CompassBG directory in Appdata with a configuration file inside it

	2. (Optional) compassbgw.lnk in Startup folder

Step 4 (Optional):
	Set up compassbgw.exe (no console version) to run at startup through either:
	
	1. Run on startup option in setup assistant

	2. Run on log on in Task Scheduler (Windows prioritises this over startup so it is faster than option 1)
		
		(My settings for Task Scheduler)
		Task scheduler:
		Trigger (Begin the task: At log on of any user)
		Action (Start a program: Program/Script: "C:\Users\me\compassbgw.exe")

## Other instructions


To remove stored app information and cache:
	Run cleardata.exe

To create the CompassBG directory manually:
	Run manualsetup.exe
