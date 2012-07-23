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
import sys, os, time

# Set up command line options and arguments
usage = "Usage: %prog [options] FILE\n\na FILE argument containing"
usage += " timestamps, azimuth, elevation, and range rate"
usage += " for a satellite pass"
parser = OptionParser(usage=usage)

parser.add_option("-s", "--host", dest="host", default="localhost",
		help="Hostname or IP address for hamlib server")
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

for tIndex in range(0, len(timestamps)):

	if time_t > timestamps[tIndex]:
		print "yup"

# after loop, park antennas
