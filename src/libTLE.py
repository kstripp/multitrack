# libTLE is designed to read in a master TLE file,
# Check/fix the checksums, and split into single TLE files.
# It may or may not take on more related functionality later.

# K. Scott Tripp <ktripp@umich.edu>
# September 2012

import sys


# SplitFile(filename) takes in a TLE file and splits it into
# files each containing a single TLE.
def SplitFile(filename):
	tle_master = open(filename, 'r')

	while True:
		line = tle_master.readline().rstrip()

		if line == '':
			break

		tle = open(line + '.txt', 'w')
		tle.write(line + '\n')
		tle.write(tle_master.readline().rstrip() + '\n')
		tle.write(tle_master.readline().rstrip() + '\n')
		tle.close()

	tle_master.close()

if __name__ == "__main__":

	SplitFile(sys.argv[1])
