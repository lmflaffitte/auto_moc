import BlynkLib, blynktimer, datetime, time, io, pynmea2, serial
from codecs import open
import sys
sys.path.insert(1, '../8relay-rpi/python/')
import lib8relay


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


### Write to LED Control Virtual Pins ###
@blynk.VIRTUAL_WRITE(1)
def rt_led_lightbar(value):
	print ('RT LED Lightbar Status: {}'.format(int(value[0])))
	lib8relay.set(1,1,int(value[0]))

@blynk.VIRTUAL_WRITE(2)
def ditch_light_led(value):
        print ('Ditch Light LED Status: {}'.format(int(value[0])))
        lib8relay.set(1,2,int(value[0]))

@blynk.VIRTUAL_WRITE(3)
def left_side_led(value):
        print ('Left Side LED Status: {}'.format(int(value[0])))
        lib8relay.set(1,3,int(value[0]))

@blynk.VIRTUAL_WRITE(4)
def right_side_led(value):
        print ('Right Side LED Status: {}'.format(int(value[0])))
        lib8relay.set(1,4,int(value[0]))

@blynk.VIRTUAL_WRITE(5)
def rear_led(value):
        print ('Rear LED Status: {}'.format(int(value[0])))
        lib8relay.set(1,5,int(value[0]))

### Alarm system handling ###

@blynk.VIRTUAL_WRITE(8)
def alarm(value):
	### fuel pump de-activation ###
	print ('Alarm Status: {}'.format(int(value[0])))
	if int(value[0]) == 1:
		print('Disabling Fuel Pump in 10 Seconds')
		time.sleep(10)
		print('Disabling Fuel Pump')
		lib8relay.set(1,8,int(value[0]))
		blynk.virtual_write(14, "DISABLED")
	else:
		lib8relay.set(1,8,int(value[0]))
		blynk.virtual_write(14, "ENABLED")

### Gather GPS Data ###
def gather_gga_data():

        ### POINTS VARIABLE TO PROPER SERIAL PORT ###
        ser = serial.Serial("/dev/serial0",9600)
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
                        print(msg)
			return lat_full, lon_full, alt, alt_unit, sats

def gather_rmc_data():
	### POINTS VARIABLE TO PROPER SERIAL PORT ###
	ser = serial.Serial("/dev/serial0",9600)
	while True:
		data = ser.readline()
		if str(data).startswith("$GNRMC"):
			### CONVERT DATA INTO LEGIBLE OUTPUTS ###
			msg = pynmea2.parse(data)
			sog = (msg.spd_over_grnd)
			print(msg)
			return sog

### SEND GPS DATA TO BLYNK###
@timer.register(vpin_num = 100, interval = 15, run_once = False)
def send_gga_data(vpin_num = 100):
	rmc_data = gather_rmc_data()
	gga_data = gather_gga_data()

	#print (str(data))
	blynk.virtual_write(20, gga_data[0])
	blynk.virtual_write(21, gga_data[1])
	blynk.virtual_write(22, gga_data[2])
	blynk.virtual_write(23, gga_data[4])
	blynk.virtual_write(24, rmc_data)


### WHILE LOOP TO RUN BLYNK ###

print('Welcome to the 4Runner MOC, powered by Raspberry Pi')
try:
	while True:
    		blynk.run()
		timer.run()

except KeyboardInterrupt:
	blynk.disconnect()
	print ('SCRIPT WAS INTERRUPTED')
