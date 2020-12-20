AutoMOC is a rasberry pi controlled python script that interfaces with a number of components in an overland vehicle. The AutoMOC script uses the Blynk IoT mobile appication which serves as the front end UI, and various relay boards, sensors, and other components that control different functions and produce telemetry around the vehicle. It also serves as a security system with GSM connectivity to notify the user if the vehicle has moved, bumped, or broken into.

AutoMOC currently can do the following:
- Using an 8 channel relay board (additional relay boards can be added), control all your LED light bars, water pumps, air compressors, kill switches, etc. 
- Provide live GPS, IMU, Altitude, Pressure, Temperature, and Battery Voltage (additional sensors can be added easily
- Arm an alarm which acts as a kill switch to the vehicle, and notifies via text the user when the vehicle has been tampered with, and sends periodic updates on GPS location 

General Configuration
- The network architecture is such that the entire AutoMOC is run offline. The rPi creates a wifi hotspot which is connected to via the mobile app. A Blynk local server is set up on the rPi. The mobile UI then commands the Blynk app all via Virtual Pins -> Python Script which pulls from the Blynk local server -> Components
- The hotspot is set up via the following: https://github.com/rudiratlos/hotspot - this script is modified to set a static IP of 10.0.0.9. A script was written to start the hotspot on boot
- A Blynk local server is set up on the rPi with the following: https://github.com/blynkkk/blynk-server, use https://www.youtube.com/watch?v=SD_ke78N7-4 as a guide
- A script was written to pipe GPS data through the USB serial port that runs on the rPi boot.

Relay Control and Mapping
The Sequent Microsystems 8Relay card has the following relays:

Relay   Power    Connections     Function
1       4A       COM, NO, NC     Fuel Pump (NC)
2       4A       COM, NO, NC     Left Side LED Pods (NO)
3       8A       COM, NO         Right Side LED Pods (NO)
4       8A       COM, NO         Ditch Lights LED Pods (NO)
5       4A       COM, NO, NC     Bumper LED Pods (NO)
6       4A       COM, NO, NC     Rooftop LED (NO) - controls a 40A relay
7       8A       COM, NO         Water Pump and Purifier(NO)
8       8A       COM, NO         GRMS Radio

Alarm System
- Once the alarm is armed, a number of functions occur:
1. After 10 seconds of arming the alarm, power is cut to the fuel pump
2. GPS location, altitude, date, and time are all saved
3. A text message is sent to the owner to verify GMS connectivity
4. If the GPS location moves by more than X meters while the alarm is active, the following occurs:
  a. A text message is sent to the owner indicating that the vehicle has moved
  b. The Ozzmaker GMS/GPS will begin streaming GPS data to InitialState.com
5. If the IMU senses a significant disturbance in its accelerometers, it will send a message to the owner indicating so



STATIC IP: 10.0.0.9

Phone and Raspberry Pi must be on same network. If this is run in the car, the Raspberry Pi must be on hotspot.


Run the AutoMoc.py Script:

$cd tools/auto_moc
$python automoc.py

Run the script in the background
$nohup python automoc.py

Cancel the script that's running in the background
$killall python

Component READMEs:
Blynk Python: https://github.com/blynkkk/lib-python 
Blynk Server: https://github.com/blynkkk/blynk-server
Mobile Hotspot: https://github.com/rudiratlos/hotspot
Relay Board: https://github.com/SequentMicrosystems/8relay-rpi
Watchdog: https://github.com/SequentMicrosystems/wdt-rpi
IMU - SPI: https://ozzmaker.com/connecting-berryimuv3-via-spi-to-a-raspberry-pi/
IMU: https://github.com/ozzmaker/BerryIMU/tree/master/python-BerryIMUv3-SPI
GPS: https://ozzmaker.com/how-to-access-gps-nema-sentences-through-usb-on-the-berrygps-gsm/
GMS - PPP: https://ozzmaker.com/berrygps-gsm-using-gps-and-connecting-via-3g-2g-using-ppp/
GMS: https://ozzmaker.com/berrygps-gsm-using-gps-and-connecting-via-3g-2g-using-ppp/
Hologram CLI: https://www.hologram.io/references/hologram-command-line-interface
