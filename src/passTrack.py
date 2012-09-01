#!/usr/bin/env python

############################################################################
# This file is part of Multitrack.                                         #
#                                                                          #
# Copyright (C) 2012 K. Scott Tripp                                        #
#                                                                          #
# AUTHORS:	K. Scott Tripp, <kscott.tripp@gmail.com>                       #
#                                                                          #
# Multitrack is free software: you can redistribute it and/or modify       #
# it under the terms of the GNU General Public License as published by     #
# the Free Software Foundation, either version 3 of the License, or        #
# (at your option) any later version.                                      #
#                                                                          #
# Multitrack is distributed in the hope that it will be useful,            #
# but WITHOUT ANY WARRANTY; without even the implied warranty of           #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
# GNU General Public License for more details.                             #
#                                                                          #
# You should have received a copy of the GNU General Public License        #
# along with Multitrack.  If not, see <http://www.gnu.org/licenses/>.      #
############################################################################

# passTrack reads in a pass file, which contains antenna vectors and
# doppler corrected frequencies.  It uses these to command the
# antenna controller and tranceiver.

from optparse import OptionParser
import ConfigParser
import sys, os, time, socket

### Parameters #############################################################
configDir = ".config/multitrack"
############################################################################

# Rotator Parameters
# This assumes that the config file exists, which *should* be reasonable
# as the multitrack main file should have already made it.
configDir = os.getenv("HOME") + "/" + configDir
conf = ConfigParser.ConfigParser()
conf.read(configDir + "/multitrack.conf")
minAz = float(conf.get("Rotator", "minAz"))
maxAz = float(conf.get("Rotator", "maxAz"))
minEl = float(conf.get("Rotator", "minEl"))
maxEl = float(conf.get("Rotator", "maxEl"))

# Set up command line options and arguments
usage = "Usage: %prog [options] FILE\n\na FILE argument containing"
usage += " timestamps, azimuth, elevation, and range rate"
usage += " for a satellite pass"
parser = OptionParser(usage=usage)

parser.add_option("-s", "--host", dest="host", default="localhost",
		help="Hostname or IP address for hamlib server")
parser.add_option("--rot-port", dest="rot_port", default="4533",
		help="Port number that rotctl is listening on")
parser.add_option("--delete", 
		action="store_true", dest="deleteFlag", default=False,
		help="Delete the pass file after use")
(options, args) = parser.parse_args()

if len(args) == 0:
	print sys.argv[0] + " must be called with one file name"
	quit()

if len(args) > 1:
	print "Error: too many arguments"
	quit()

# Pass File Column Configuration
timeCol = 0
azCol = 1
elCol = 2
rateCol = 3


### Read in pass data ######################################################
passFile = open(args[0], 'r')
passFile.readline() #discard header

timestamps = []
azimuth = []
elevation = []
range_rate = []
for line in passFile:
	waypoint = line.split(' ')
	timestamps.append(int(waypoint[timeCol]))
	azimuth.append(float(waypoint[azCol]))
	elevation.append(float(waypoint[elCol]))
	range_rate.append(float(waypoint[rateCol].split('\n')[0]))

# Delete old pass file
if options.deleteFlag:
	os.remove(args[0])
	print "Deleted " + args[0]

### Loop through pass based on timestamps ##################################
time_t = time.time()

# Set up Socket
BUFFER_SIZE = 256
rotator = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rotator.connect((options.host, int(options.rot_port)))

# Slew antennes before pass starts
# TODO: adjust the file so that the azimuth tracks below horizon
if maxAz <= azimuth[0]:
	rotator.send("P " + str(int(azimuth[0]-360)) + " 000")
	print "P " + str(int(azimuth[0]-360)) + " 000"
else:
	rotator.send("P " + str(int(azimuth[0])) + " 000")
	print "P " + str(int(azimuth[0])) + " 000"

# Loop through timestamps in pass
tIndex = 0
while tIndex < len(timestamps)-1:

	# Fast forward if pass has already started
	if time_t <- timestamps[tIndex+1]:
		tIndex+=1

	elif time_t >= timestamps[tIndex]:
		
		if azimuth[tIndex] <= maxAz:
			setAz = str(int(azimuth[tIndex]))
		else:
			setAZ = str(int(azimuth[tIndex]-360))

		setAz = setAz.zfill(3)
		setEl = str(int(elevation[tIndex])).zfill(3)
		rotString = "P " + setAz + ' ' + setEl

		print rotString
		rotator.send(rotString)
		tIndex+=1
	
	time.sleep(0.5)
	time_t = time.time()
	print timestamps[tIndex]
	print time_t

# after loop, park antennas
time.sleep(120)
if 270 > maxAz:
	rotator.send("P -090 000")
else:
	rotator.send("P 270 000")
rotator.close()
