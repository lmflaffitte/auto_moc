AutoMOC is a rasberry pi controlled python script that interfaces with a number of components in an overland vehicle. The AutoMOC script uses the Blynk IoT mobile appication which serves as the front end UI, and various relay boards, sensors, and other components that control different functions and produce telemetry around the vehicle. It also serves as a security system with GSM connectivity to notify the user if the vehicle has moved, bumped, or broken into.

AutoMOC currently can do the following:
- Using an 8 channel relay board (additional relay boards can be added), control all your LED light bars, water pumps, air compressors, kill switches, etc. 
- Provide live GPS, IMU, Altitude, Pressure, Temperature, and Battery Voltage (additional sensors can be added easily
- Arm an alarm which acts as a kill switch to the vehicle, and notifies via text the user when the vehicle has been tampered with, and sends periodic updates on GPS location 

General Configuration
- The network architecture is such that the entire AutoMOC is run offline. The rPi creates a wifi hotspot which is connected to via the mobile app. A Blynk local server is set up on the rPi. The mobile UI then commands the Blynk app all via Virtual Pins -> Python Script which pulls from the Blynk local server -> Components
- The hotspot is set up via the following: https://github.com/rudiratlos/hotspot - this script is modified to set a static IP of 10.0.0.9
- A Blynk local server is set up on the rPi with the following: https://github.com/blynkkk/blynk-server, use https://www.youtube.com/watch?v=SD_ke78N7-4 as a guide

STATIC IP: 10.0.0.9

Run the AutoMoc.py Script:

$cd tools/auto_moc
$python automoc.py

Run the script in the background
$nohup python automoc.py

Cancel the script that's running in the background
$killall python

