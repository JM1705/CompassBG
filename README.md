# CompassBG
Create and set a background with the Compass schedule for the day

Dependencies:

	Windows 10 (11 would probably work as well)

	Python 3.10 (For CfgCreate.py)

	Json (For CfgCreate.py)

Instructions:

Step 1:
	Create a directory with wallpaper images

Step 2:
	Create a configuration file either through the CfgCreate.py script or by editing the json yourself 
	(the json file has advanced properties that aren't accessible from the script)

Step 3:
	Set up the main exe file to run whenever you want through Task Scheduler
	
	(My settings)
	Task scheduler:
	Trigger (Begin the task: At log on of any user)
	Action (Start a program: Program/Script: "C:\Users\me\CompassBG.exe")
