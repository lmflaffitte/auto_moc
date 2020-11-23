import BlynkLib
from datetime import datetime
import sys
#sys.path.insert(1,'../relay8-rpi/python/')
#import relay8


#initialize Blynk
blynk = BlynkLib.Blynk('SngWfLytk3BxQcrVcj0X483pwGq2XRwU')

#Register Virtual Pin
@blynk.VIRTUAL_READ(2)
def my_read_handler():
	currentTime = datetime.now()
	blynk.virtual_write(2, currentTime.strftime("%d/%m/%Y %H:%M:%S"))

@blynk.VIRTUAL_WRITE(1)
def my_write_handler(value):
	relay8.set(1, 1, value)
	print('Current V1 value: {}'.format(value))


print ("started!")
while True:
	blynk.run()
