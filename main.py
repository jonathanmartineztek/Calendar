#!/usr/bin/env python
#https://repl.it/@jonathanmartinez/DeficientOutstandingFibonacci
import ephem #pip install pyephem
import datetime
import os
from pytz import timezone

logPath = os.path.expanduser('~') + "/Documents/1og.txt"
now_utc = datetime.datetime.utcnow().replace(tzinfo=timezone('UTC'))
next_utc = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).replace(tzinfo=timezone('UTC'))
previousNewMoon = (ephem.previous_new_moon(now_utc).datetime().replace(tzinfo=timezone('UTC')))
prevNewMoon = (ephem.previous_new_moon(previousNewMoon).datetime().replace(tzinfo=timezone('UTC')))
nextNewMoon = (ephem.next_new_moon(now_utc).datetime().replace(tzinfo=timezone('UTC')))

def getObserver():
	home = ephem.Observer()
	home.lat = "33.98"
	home.lon = "-117.37"
	home.elevation = 260
	#To get U.S. Naval Astronomical Almanac values, use these settings
	home.pressure = 0
	home.horizon = "-0:34"

	return home

def readLog():
	inFile = open("log.txt")
	try:
		global chodesh

		content = inFile.readlines()
		log = content[len(content)-1].split(";")
		chodesh = getChodesh(log[0])
	except:
		raise ValueError(logPath)
	finally:
		inFile.close()

def getIllumination(date = now_utc):
	home = getObserver()
	home.date = date
	moon = ephem.Moon()
	moon.compute(home)
	return round(float(moon.moon_phase * 100),1)

def getRoshChodesh(date = previousNewMoon):
	found = False#True
	rosh = date
	while not found:
		rosh = getSunset(rosh)
		illumination = getIllumination(rosh)
		if illumination <= 1.5:
			found = False
			getSunset(rosh)
		else:
			found = True
	return rosh if now_utc >= rosh else getRoshChodesh(prevNewMoon)

def getSunset(date = now_utc):
	home = getObserver()
	home.date = date
	sun = ephem.Sun()
	sun.compute(home)
	nextSunset = home.next_setting(sun).datetime().replace(tzinfo=timezone('UTC'))
	return nextSunset

def utc2pacific(datetime):
	return datetime.astimezone(timezone('US/Pacific'))

def getDaySince():
	return (now_utc.date() - utc2pacific(getRoshChodesh()).date()).days

def getChodesh(num):
	#input <type 'str'>
	chodeshim = { '1': 'Nisan', '2': 'Iyar', '3': 'Sivan', '4': 'Tammuz', '5': 'Av', '6': 'Elul',
		'7': 'Tishrei', '8': 'Cheshvan', '9': 'Kislev', '10': 'Tevet', '11': 'Shevat', '12': 'Adar', '13': 'Adar II'}
	try:
		chodesh = chodeshim[num.strip()]

		#return <type 'str'>
		return chodesh
	except:
		raise ValueError('Not a month')

readLog()
print( chodesh + " " + str(getDaySince()) + " (" + str(getIllumination()) + "%)")
print("---")
#print("Moon Illumination: " + str(getIllumination()) + "%")
print("Sunset:")
#if now_utc < getSunset():
print("Next (" + utc2pacific(getSunset()).strftime("%x): %X %Z%z"))
#else:
print("Next (" + utc2pacific(getSunset(next_utc)).strftime("%x): %X %Z%z"))

print("---")
print("New Moon:")
print("Prev (" + previousNewMoon.strftime("%x): %X %Z%z(") + str(getIllumination(previousNewMoon)) + "%)")
print("Next (" + nextNewMoon.strftime("%x): %X %Z%z(") + str(getIllumination(nextNewMoon)) + "%)")
