import BlynkLib
from datetime import datetime
import sys
sys.path.insert(1, '../relay8-rpi/python/')
import relay8


# Initialize Blynk
blynk = BlynkLib.Blynk('SngWfLytk3BxQcrVcj0X483pwGq2XRwU')

# Register Virtual Pins
@blynk.VIRTUAL_WRITE(1)
def my_write_handler(value):
	print('Current V1 value: {}'.format(value))
	relay8.set(1,1,int(value[0]))

@blynk.VIRTUAL_READ(2)
def my_read_handler():
    # this widget will show some time in seconds..
    blynk.virtual_write(2, int(time.time()))

while True:
    blynk.run()
