import BlynkLib, blynktimer, datetime, time, io, pynmea2, serial, threading
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
blynk = BlynkLib.Blynk('LvtQ5eL-1to3mBm8GXblYgoqPAjZm4zH',
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
@blynk.VIRTUAL_WRITE(6)
def rt_led_lightbar(value):
	print ('RT LED Lightbar Status: {}'.format(int(value[0])))
	lib8relay.set(1,6,int(value[0]))

@blynk.VIRTUAL_WRITE(4)
def ditch_light_led(value):
        print ('Ditch Light LED Pods Status: {}'.format(int(value[0])))
        lib8relay.set(1,4,int(value[0]))

@blynk.VIRTUAL_WRITE(2)
def left_side_led(value):
        print ('Left Side LED Pods Status: {}'.format(int(value[0])))
        lib8relay.set(1,2,int(value[0]))

@blynk.VIRTUAL_WRITE(3)
def right_side_led(value):
        print ('Right Side LED Pods Status: {}'.format(int(value[0])))
        lib8relay.set(1,3,int(value[0]))

@blynk.VIRTUAL_WRITE(5)
def rear_led(value):
        print ('Rear LED Pods Status: {}'.format(int(value[0])))
        lib8relay.set(1,5,int(value[0]))

### Water Pump and UV Filter Powering ###

@blynk.VIRTUAL_WRITE(7)
def rear_led(value):
        print ('Water Pump and UV Filter Power: {}'.format(int(value[0])))
        lib8relay.set(1,7,int(value[0]))


### Alarm system handling ###

@blynk.VIRTUAL_WRITE(8)
def alarm(value):
	current_date = datetime.datetime.now()
	hologram = HologramCloud(None, network='cellular')
	### fuel pump de-activation ###
	print ('Alarm Status: {}'.format(int(value[0])))
	if int(value[0]) == 1:
		print('Disabling Fuel Pump in 10 Seconds')
		time.sleep(10)
		print('Disabling Fuel Pump')
		lib8relay.set(1,8,int(value[0]))
		blynk.virtual_write(14, "DISABLED")
		blynk.virtual_write(13, current_date.strftime("%Y-%m-%d %H:%M:%S"))
		### print GPS Static data ###
		gps_data = gather_gps_data()
		vehicle_lat = gps_data[0]
		vehicle_lon = gps_data[1]
		vehicle_alt = gps_data[2]
		blynk.virtual_write(25, vehicle_lat)
		blynk.virtual_write(26, vehicle_lon)
		blynk.virtual_write(35, vehicle_alt)
	else:
		lib8relay.set(1,8,int(value[0]))
		blynk.virtual_write(14, "ENABLED")

### Gather GPS Data ###

def gather_gps_data():
	lat = gather_gpsd.readCoordinates()[0]
	lon = gather_gpsd.readCoordinates()[1]
	alt = gather_gpsd.readCoordinates()[2]
	speed = gather_gpsd.readCoordinates()[3]
	climb = gather_gpsd.readCoordinates()[4]
	fixtype = gather_gpsd.readCoordinates()[6]

	gps_data = [lat, lon, alt, speed, climb, fixtype]
	return gps_data

def gather_gga_data():
        ### POINTS VARIABLE TO PROPER SERIAL PORT ###
        ser = serial.Serial("/dev/ttyACM3",115200)
        ### WHILE LOOP TO KEEP READING DATA-STREAM ###
        while True:
                data = ser.readline()
                if str(data).startswith("$GNGGA"):

                        ### CONVERT DATA INTO LEGIBLE OUTPUTS###
			msg = pynmea2.parse(data)
                       #lat = (round(msg.latitude, 5))
                        lat = ('%02d{}%02d\'%07.4f'.format(" ") % (msg.latitude, msg.latitude_minutes, msg.latitude_seconds))
			lat_dir = (msg.lat_dir)
			lat_full = lat + " " + lat_dir
                       #lon = (round(msg.longitude, 5))
                        lon = ('%02d{}%02d\'%07.4f'.format(" ") % (msg.longitude, msg.longitude_minutes, msg.longitude_seconds))
			lon_dir = (msg.lon_dir)
			lon_full = lon + " " + lon_dir
                        alt = (msg.altitude)
                        alt_unit = (msg.altitude_units)
                        sats = (msg.num_sats)
                        #print(msg)
			return lat_full, lon_full, alt, alt_unit, sats

def gather_rmc_data():

	### POINTS VARIABLE TO PROPER SERIAL PORT ###
	ser = serial.Serial("/dev/ttyACM3",115200)
	while True:
		data = ser.readline()
		if str(data).startswith("$GNRMC"):
			### CONVERT DATA INTO LEGIBLE OUTPUTS ###
			msg = pynmea2.parse(data)
			sog = (msg.spd_over_grnd)
			#print(msg)
			return sog

### SEND GPS DATA TO BLYNK ###
@timer.register(vpin_num = 100, interval = 5, run_once = False)
def send_gps_data(vpin_num = 100):
	gps_data = gather_gps_data()

	#print (str(data))
	blynk.virtual_write(20, gps_data[0])
	blynk.virtual_write(21, gps_data[1])
	blynk.virtual_write(22, gps_data[2])
	blynk.virtual_write(23, gps_data[3])
	blynk.virtual_write(24, gps_data[4])



### SEND IMU DATA TO BLYNK ###
@timer.register(vpin_num = 101, interval = 1, run_once = False)
def send_imu_data(vpin_num = 101):
	AccXangle = berryIMUspi.get_imu_data()[0]
	AccYangle = berryIMUspi.get_imu_data()[1]
	gyroXangle = berryIMUspi.get_imu_data()[2]
	gyroYangle = berryIMUspi.get_imu_data()[3]
	gyroZangle = berryIMUspi.get_imu_data()[4]
	CFangleX = berryIMUspi.get_imu_data()[5]
	CFangleY = berryIMUspi.get_imu_data()[6]
	ACCx = berryIMUspi.get_imu_data()[7]
	ACCy = berryIMUspi.get_imu_data()[8]
	ACCz = berryIMUspi.get_imu_data()[9]

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
