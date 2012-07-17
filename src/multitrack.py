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
numHours = 24		# interval that this script should be run
startDelay = 5		# minutes before pass starts
configDir = "~/.config/multitrack"
#######################################

# Read in satellites to track
conf = ConfigParser.ConfigParser()
conf.read("multitrack.conf")
satSet =  conf.items("Sats")

sats = []
for pair in satSet:
	sats.append(str.upper(pair[0]))

# Fetch and parse TLE File
os.system("./tleupdate")


# Set up time variables
time_t = time.time()
tlocal = time.asctime()

predictionURL=predictionURL+sats[0]
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

# iterate passes in the next 12 hours
numPasses = 0
while numPasses < maxPasses:
	satpass =  pred.readline().split('&')
	passtime = time.strptime(satpass[aos_col] + " UTC", '%Y/%m/%d %H:%M:%S %Z')
	lostime = time.strptime(satpass[los_col] + " UTC", '%Y/%m/%d %H:%M:%S %Z')

	# Conver UTC time struct to UNIX
	passtime = calendar.timegm(passtime)
	lostime = calendar.timegm(lostime)

	# Check that pass is within planned interval
	if passtime > time_t + 60*60*numHours:
		break
	
	print str(passtime) + ' ' + str(lostime)

	# Convert UNIX time to local time struct
	passtime = time.localtime(passtime)

	# Build Command string
	cmdString = configDir + "/restart_client.cron"
	timeStr = time.strftime('%R %D', passtime)
	cmdString = 'echo "' + cmdString +  '" | at ' + timeStr

	# Execute String
	#os.system(cmdString)


	numPasses += 1

# clean up
pred.close()
