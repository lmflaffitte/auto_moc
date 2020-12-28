import blynklib, blynktimer, datetime, time, io, serial, threading, math
from geopy import distance
from codecs import open
import sys
sys.path.insert(1, '../8relay-rpi/python/')
import lib8relay
sys.path.insert(1, '../BerryIMU/python-BerryIMUv3-SPI')
import berryIMUspi, IMU
import gather_gpsd
from Hologram.HologramCloud import HologramCloud
from ISStreamer.Streamer import Streamer

### Initialize Blynk ###
blynk = blynklib.Blynk('ge_FQJIPSVaAhQXvsCw8gMW-LwXmZNZx',
			server='10.0.0.9',
			port=8080,
			heartbeat=30
			#log=print
			)

### Create Timers Dispatcher Instance ###
timer = blynktimer.Timer()


### Define Global Variables ###
degree_sign = u"\N{DEGREE SIGN}"
gpsd = None

### Write to LED Control Virtual Pins ###
@blynk.handle_event('write V6')
def rt_led_lightbar(pin,value):
	print ('RT LED Lightbar Status: {}'.format(int(value[0])))
	lib8relay.set(1,6,int(value[0]))

@blynk.handle_event('write V4')
def ditch_light_led(pin,value):
        print ('Ditch Light LED Pods Status: {}'.format(int(value[0])))
        lib8relay.set(1,4,int(value[0]))

@blynk.handle_event('write V2')
def left_side_led(pin,value):
        print ('Left Side LED Pods Status: {}'.format(int(value[0])))
        lib8relay.set(1,2,int(value[0]))

@blynk.handle_event('write V3')
def right_side_led(pin,value):
        print ('Right Side LED Pods Status: {}'.format(int(value[0])))
        lib8relay.set(1,3,int(value[0]))

@blynk.handle_event('write V5')
def rear_led(pin,value):
        print ('Rear LED Pods Status: {}'.format(int(value[0])))
        lib8relay.set(1,5,int(value[0]))

### Water Pump and UV Filter Powering ###

@blynk.handle_event('write V7')
def rear_led(pin,value):
	print ('Water Pump and UV Filter Power: {}'.format(int(value[0])))
	lib8relay.set(1,7,int(value[0]))


### GMRS Radio Power ###
@blynk.handle_event('write V8')
def gmrs_power(pin,value):
	print ('GMRS Radio Power: {}'.format(int(value[0])))
	lib8relay.set(1,7,int(value[0]))


### Alarm system handling ###

@blynk.handle_event('write V1')
def alarm(pin,value):
	print('Alarm Status: {}'.format(int(value[0])))
	current_date = datetime.datetime.now()
	credentials = {'devicekey': 'LMaCQ?]G'}
	hologram = HologramCloud(credentials, network='cellular', authentication_type='csrpsk')


	### fuel pump de-activation ###
	if int(value[0]) == 1:
		print ('Disabling Fuel Pump in 10 Seconds')
		time.sleep(10)
		print ('Disabling Fuel Pump')
		lib8relay.set(1,1,int(value[0]))
		blynk.virtual_write(14, "DISABLED")
		blynk.virtual_write(13, current_date.strftime("%Y-%m-%d %H:%M:%S"))

		### gather/write GPS vehicle data ###
		vehicle_lat = gather_gps_data()[0]
		vehicle_lon = gather_gps_data()[1]
		vehicle_alt = gather_gps_data()[2]
		blynk.virtual_write(25, vehicle_lat)
		blynk.virtual_write(26, vehicle_lon)
		blynk.virtual_write(35, vehicle_alt)
		vehicle_location = (vehicle_lat, vehicle_lon)

		print (vehicle_location)

		### send activation SMS ###
		recv = hologram.sendSMS('+12069725002', 'AutoMOC Alarm Enabled. System has confirmed network connectivity')
		print ('RESPONSE MESSAGE: ' + hologram.getResultString(recv))

		### start geofence alarm ###
		timer.start('run_geofence_alarm(vehicle_location)')
	else:
		timer.stop('run_geofence_alarm')
		timer.stop('stream_gps')
		print ('Alarm toggled off')
		lib8relay.set(1,1,int(value[0]))
		blynk.virtual_write(14, "ENABLED")

### Alarm Timers ###

@timer.register(vpin_num = 103, interval = 10, stopped = True)
def run_geofence_alarm(vpin_num = 103, vehicle_location):
        print('Geofence Check')
        current_location = (gather_gps_data()[0], gather_gps_data()[0])
        print (current_location)
        displacement = distance.distance(vehicle_location, current_location).km
        print(displacement + 'km')
        alarm_trigger = .02
        if displacement > alarm_trigger:
                print('Geofence Alarm TRIPPED')
                alarm_recv = hologram.sendSMS('+12069725002', 'AutoMOC Geofence Alarm TRIPPED. Go to InitialState.com for real-time tracking updates.')
                print('RESPONSE MESSAGE: ' + hologram.getResultString(alarm_recv))
                timer.start('stream_gps()')
                timer.stop('run_geofence_alarm()')
        else:
                print('Alarm not tripped, continuing period checks')


@timer.register(vpin_num = 104, interval = 10, stopped = True)
def stream_gps(vpin_num = 104):
        print('Streaming data to InitialState.com')
        print 'CPU time->',datetime.datetime.now().time() ,
        streamer.log("Location", "{lat},{lon}".format(lat=gather_gps_data()[0],lon=gather_gps_data()[1]))
        streamer.log("speed",gather_gps_data()[3])



### Gather GPS Data ###

def gather_gps_data():
	lat = gather_gpsd.readCoordinates()[0]
	lon = gather_gpsd.readCoordinates()[1]
	alt = gather_gpsd.readCoordinates()[2]
	speed = gather_gpsd.readCoordinates()[3]
	climb = gather_gpsd.readCoordinates()[4]
	track = gather_gpsd.readCoordinates()[5]
	utc_time = gather_gpsd.readCoordinates()[6]

	gps_data = [lat, lon, alt, speed, climb, track, time]
	return gps_data

### SEND GPS DATA TO BLYNK ###
@timer.register(vpin_num = 100, interval = 5, run_once = False)
def send_gps_data(vpin_num = 100):
	gps_data = gather_gps_data()

	#print (str(data))
	blynk.virtual_write(20, round(gps_data[0],5))
	blynk.virtual_write(21, round(gps_data[1],5))
	blynk.virtual_write(22, gps_data[2])
	blynk.virtual_write(23, gps_data[3])
	blynk.virtual_write(24, gps_data[4])
	blynk.virtual_write(33, gps_data[5])



### SEND IMU DATA TO BLYNK ###
@timer.register(vpin_num = 101, interval = 1, run_once = False)
def send_imu_data(vpin_num = 101):
	AccXangle = round(berryIMUspi.get_imud()[0],1)
	AccYangle = round(berryIMUspi.get_imud()[1],1)
	gyroXangle = berryIMUspi.get_imud()[2]
	gyroYangle = berryIMUspi.get_imud()[3]
	gyroZangle = berryIMUspi.get_imud()[4]
	CFangleX = berryIMUspi.get_imud()[5]
	CFangleY = berryIMUspi.get_imud()[6]
	ACCx = berryIMUspi.get_imud()[7]
	ACCy = berryIMUspi.get_imud()[8]
	ACCz = berryIMUspi.get_imud()[9]

	#write Blynk data
	blynk.virtual_write(30, AccXangle)
	blynk.virtual_write(31, AccYangle)
	blynk.virtual_write(32, ACCx)
	blynk.virtual_write(33, ACCy)
	blynk.virtual_write(34, ACCz)


### GATHER HOLOGRAM DATA ###

def gather_hologram_data():
	hologram = HologramCloud(None, network='cellular')
	signal_strength = hologram.network.signal_strength
	operator = hologram.network.operator
	rssi, qual = signal_strength.split(',')
	return rssi, qual, operator

### SEND GMS DATA TO BLYNK ###

@timer.register(vpin_num = 102, interval = 30, run_once = False)
def send_gms_data(vpin_num = 102):
	### print GMS data ###
	rssi = gather_hologram_data()[0]
	qual = gather_hologram_data()[1]
	operator = gather_hologram_data()[2]
	blynk.virtual_write(27, rssi)
	blynk.virtual_write(28, qual)
	blynk.virtual_write(29, operator)


### WHILE LOOP TO RUN BLYNK ###

print('Welcome to the 4Runner MOC, powered by Raspberry Pi')

try:
	while True:
    		blynk.run()
		timer.run()

except KeyboardInterrupt:
	blynk.disconnect()
	gather_gpsd.kill_thread()
	print ('SCRIPT WAS INTERRUPTED')
