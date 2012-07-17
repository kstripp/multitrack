#!/usr/bin/env python

# passTrack reads in a pass file, which contains antenna vectors and
# doppler corrected frequencies.  It uses these to command the
# antenna controller and tranceiver.
#
# K. Scott Tripp <ktripp@umich.edu>

from optparse import OptionParser
import sys

# Set up command line options and arguments
parser = OptionParser()
parser.add_option("-s", "--host", dest="host", default="localhost",
		help="Hostname or IP address for hamlib server")
(options, args) = parser.parse_args()

if len(args) == 0:
	print sys.argv[0] + " must be called with at least one file name"
	quit()

passFile = args[0]

