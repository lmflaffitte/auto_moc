import BlynkLib
from datetime import datetime
import sys
sys.path.insert(1, '../8relay-rpi/python/')
import lib8relay


# Initialize Blynk
blynk = BlynkLib.Blynk('SngWfLytk3BxQcrVcj0X483pwGq2XRwU')

print('Welcome to the 4Runner MOC, powered by Raspberry Pi')

# Write to LED Control Virtual Pins
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

#Alarm system handling

@blynk.VIRTUAL_WRITE(8)
def rear_led(value):
	#fuel pump de-activation
	print ('Alarm Status: {}'.format(int(value[0])))
        lib8relay.set(1,8,int(value[0]))



@blynk.VIRTUAL_READ(10)
def my_read_handler():
    # this widget will show some time in seconds..
    blynk.virtual_write(2, int(time.time()))

while True:
    blynk.run()
