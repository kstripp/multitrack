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

