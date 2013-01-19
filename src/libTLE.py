# libTLE is designed to read in a master TLE file,
# Check/fix the checksums, and split into single TLE files.
# It may or may not take on more related functionality later.

# K. Scott Tripp <ktripp@umich.edu>
# September 2012

# multitrack configuration variables
import config

# python standard libraries
import sys
import os
import time

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

#####################################################################
# update()
#####################################################################
def update(tleDir, conf):
	"""
	update(tleDir, conf) --> none
	checkes the elapsed time since the last TLE update,
	and runs an update if it has been longer than 24 hours
	"""

	interval = 86400 # seconds per day

	if time.time() - update.last_update > interval:

		# TODO: if tleupdate did *not* succeed, last_update should
		# not be updated.
		os.system("tleupdate -d " + tleDir)
		SplitFile(tleDir + "/" + conf.get("TLE", "tle"), 0, tleDir)
		update.last_update = time.time()

# initialize last_update timestamp.
# this forces it to run on first call.
update.last_update = 0

if __name__ == "__main__":

	SplitFile(sys.argv[1])
