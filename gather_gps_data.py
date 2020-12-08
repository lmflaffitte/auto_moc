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
                        lat = ('%02d{}%02d\'%07.4f'.format(" ") % (msg.latitude, msg.latitude_minutes, msg.latitude_$                        lat_dir = (msg.lat_dir)
                        lat_full = lat + " " + lat_dir
                       #lon = (round(msg.longitude, 5))
                        lon = ('%02d{}%02d\'%07.4f'.format(" ") % (msg.longitude, msg.longitude_minutes, msg.longitu$                        lon_dir = (msg.lon_dir)
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
