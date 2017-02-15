# Blynk-Home-Monitor
Node.js/Python home automation project using Blynk and a Raspberry Pi Model B (Rev. 2)

Roadmap:

I have two Raspberry Pi's: 

	Model B Rev. 2 (Reused Kano board) with a PiTFT, tactile buttons, DHT22 temperature/humidity sensor, and a Powerswtich Tail 2. 
	Model 3 B with a SenseHat, DHT22 temperature/humidity sensor, and a NoIR PiCam.
	
The plan is to use a combination of node.js with Blynk and Python scripts to monitor the temperature in my apartment and warn me if it's getting too hot for my kitty, and to automate some home lighting based on local sunset times and when I'm likely to go to bed. The display and buttons will be used for in-home monitoring and manual overrides for the lighting.
For the PiCam, I'll probably create some kind of home security camera if I can get the security right.

I'll be using Python3 for most of the hands-off automated work and node.js where interfacing with Blynk is needed.

NB: I am a completely novice coder, I'm using GitHub to hopefully learn some good revisioning habits and to preserve my ideas. Things might work, they might not. 
