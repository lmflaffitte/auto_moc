import os
import time
import math
import threading
from gps import *

gpsd = None #seting the global variable

class GpsPoller(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		global gpsd #bring it in scope
		gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
		self.current_value = None
		self.running = True #setting the thread running to true

	def run(self):
		global gpsd
		while gpsp.running:
			gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

gpsp = GpsPoller() # create the thread

print "\nStarting GPS Thread"
gpsp.start() #start the thread

def readCoordinates():

	lat = gpsd.fix.latitude
	lon = gpsd.fix.longitude
	speed = gpsd.fix.speed
	alt = gpsd.fix.altitude
	climb = gpsd.fix.climb
	track = gpsd.fix.track
	fixtype = gpsd.fix.mode
	coords = [lat, lon, alt, speed, climb, track, fixtype]

	return coords

def kill_thread():
	print "\nKilling GPS Thread..."
	gpsp.running = False
	gpsp.join() #wait for thread to finish what it's doing
