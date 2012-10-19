# libTLE is designed to read in a master TLE file,
# Check/fix the checksums, and split into single TLE files.
# It may or may not take on more related functionality later.

# K. Scott Tripp <ktripp@umich.edu>
# September 2012

import sys


# SplitFile(filename) takes in a TLE file and splits it into
# files each containing a single TLE.
def SplitFile(filename, name_flag=1, outputDir=''):
	tle_master = open(filename, 'r')

	if outputDir == '':
		outputDir = '.'

	while True:
		line = tle_master.readline().rstrip()

		if line == '':
			break

		sat_name = (line + '\n')
		line1 = (tle_master.readline().rstrip() + '\n')
		line2 = (tle_master.readline().rstrip() + '\n')

		sat_num = line1[2:7] #From TLE specification
		
		if name_flag:
			tle = open(outputDir + "/" + line + '.txt', 'w')
		else:
			tle = open(outputDir + "/" + str(sat_num) + '.txt', 'w')

		tle.write(sat_name)
		tle.write(line1)
		tle.write(line2)
		tle.close()

	tle_master.close()

if __name__ == "__main__":

	SplitFile(sys.argv[1])
