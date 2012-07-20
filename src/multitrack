#!/usr/bin/env python

# This script is designed to run as a daily cron job.  It updates the
# local TLE database and then schedules passes for each tracked satellite.

import ConfigParser

import os, urllib2, time, calendar

### Parameters ########################
maxPasses = 10
predictionURL = "http://gs.engin.umich.edu/predictions2/ANN_ARBOR/"
aos_col = 0
los_col = 2
orbNum_col = 9
numHours = 24		# interval that this script should be run
startDelay = 5		# minutes before pass starts
configDir = "~/.config/multitrack"
#######################################

# TODO: add check for config file, if it doesn't exist create one from the sample
if os.path.exists(configDir + "/multitrack.conf"):
	print "Using config file " + configDir + "/multitrack.conf"
else:
	print "Copying example config file to " + configDir
	os.system("cp /usr/local/etc/multitrack/multitrack.conf " + configDir)

# Read in satellites to track
conf = ConfigParser.ConfigParser()
conf.read(configDir + "/multitrack.conf")
print conf.sections()
satSet = conf.items("Sats")

sats = []
for pair in satSet:
	sats.append(str.upper(pair[0]))

# Fetch and parse TLE File
os.system("tleupdate -d " + configDir)


# Set up time variables
time_t = time.time()
tlocal = time.asctime()

# TODO: Loop through Satellites
sat = sats[1]
predictionURL=predictionURL+sat
try:
	pred = urllib2.urlopen(predictionURL)
except urllib2.URLError:
	msg = tlocal + ": URL Error, client restarts not scheduled"
	print msg
	os.system("echo " + msg + " >> errlog.txt")
	quit()
except urllib2.HTTPError:
	msg = str(tlocal) + ": HTTP Error, client restarts not scheduled"
	os.system("echo " + msg + " >> errlog.txt")
	quit()

# iterate passes in the next 24 hours
numPasses = 0
while numPasses < maxPasses:
	satpass =  pred.readline().split('&')
	passtime = time.strptime(satpass[aos_col] + " UTC", '%Y/%m/%d %H:%M:%S %Z')
	lostime = time.strptime(satpass[los_col] + " UTC", '%Y/%m/%d %H:%M:%S %Z')
	orbitNum = satpass[orbNum_col].split('\n')[0].split(' ')[1]

	# Conver UTC time struct to UNIX
	passtime = calendar.timegm(passtime)
	lostime = calendar.timegm(lostime)

	# Check that pass is within planned interval
	if passtime > time_t + 60*60*numHours:
		break

	# Call pass prediction
	cmdString =  "multitrack -a " + str(passtime) + ' -l ' + str(lostime)
	cmdString = cmdString + " -o " + configDir + "/" + orbitNum + "_AA_" + sat + ".txt"
	print cmdString

	# Convert UNIX time to local time struct
	passtime = time.localtime(passtime)

	# Build Command string
	cmdString = "passTrack.py " + configDir + "/" + orbitNum + "_AA_" + sat + ".txt" 
	timeStr = time.strftime('%R %D', passtime)
	cmdString = 'echo "' + cmdString +  '" | at ' + timeStr

	# Execute String
	#os.system(cmdString)

	print cmdString

	numPasses += 1

# clean up
pred.close()
