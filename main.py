#!/usr/bin/env python

import ephem #pip install pyephem
import datetime
import os
from pytz import timezone
import urllib2

currentDate = datetime.datetime.now(timezone("US/Pacific"))
nextDate = currentDate + datetime.timedelta(days=1)
spottedAfter = 1

def display():
	global home
	
	home = ephem.Observer()
	home.lat = "33.98"
	home.lon = "-117.37"
	home.elevation = 260
	#To get U.S. Naval Astronomical Almanac values, use these settings
	home.pressure = 0
	home.horizon = "-0:34"

	readLog()
	if onLine():
		if len(logB) == 3:
			print(chodesh + " " + str(yom))
		elif len(logB) == 2:
			getNewMoon()
			print(chodesh + " " + str(yom))
	elif not onLine():
		if len(logB) == 3:
			print(chodesh + " " + str(yom) + "*")
		else:
			print("offLine")

def onLine():
	try:
		urllib2.urlopen('http://www.google.com', timeout=1)
		return True
	except urllib2.URLError as err:
		return False

def readLog():
	global log
	
	log = os.path.expanduser('~') + "/Documents/t/log.txt" 
	#'/Users/mrsir' + 'Documents/t/log/txt'
	inFile = open(log)
	try:
		global chodesh
		global yyyymm
		global year
		global month
		global day
		global logB

		content = inFile.readlines()
		log = content[len(content)-1].split(";")

		chodesh = getChodesh(log[0])
		yyyymm = log[1]

		logB = log[1].split("/")
		year = int(logB[0])
		month = int(logB[1])
		if len(logB) == 3:
			day = int(logB[2])
			roshChodesh = datetime.date(year, month, day+spottedAfter)
			getDaysSince(roshChodesh)

	finally:
		inFile.close()

def updateLog(update):
	if len(logB) == 2:
		inFile = open(log, "a")
		try:
			inFile.write(update)
		finally:
			inFile.close()

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

def getDaysSince(roshChodesh):
	global yom
	
	to_day = datetime.date(currentDate.year,currentDate.month, currentDate.day)
	yom = (to_day - roshChodesh).days + isNowInTimePeriod()

def getNewMoon():
	global yyyymm
	
	n = str(ephem.next_new_moon(yyyymm))
	# 2018/10/9 03:46:51
	n = n.split(" ")
	# ["2018/10/9", "03:46:51"]
	n = n[0].split("/")
	#["2018", "10", "9"]
	updateLog("/" + n[2])
	readLog()

	#return <type 'datetime.date'>
	return datetime.date(int(n[0]), int(n[1]), int(n[2]) + spottedAfter)

def getIllumination():
	moon = ephem.Moon()
	moon.compute(home)

	return float(moon.moon_phase * 100)

def getSunseTime():
	global sunseTime
	
	sun = ephem.Sun()
	sun.compute(nextDate.strftime("%Y/%m/%d"))
	nowSet = home.next_setting(sun).datetime()
	nowSetUTC = naive2aware(nowSet) #<type 'datetime.datetime'>
	nowSetPacific = UTC2Pacific(nowSetUTC)
	sunseTime = nowSetPacific.strftime("%X")

	#return <type 'str'>
	return nowSetPacific

def naive2aware(date):
	return timezone("UTC").localize(date)

def UTC2Pacific(time):
	return time.astimezone(timezone('US/Pacific'))

def isNowInTimePeriod():
	nextSet = getSunseTime()
	toDate = currentDate.replace(currentDate.year,currentDate.month,currentDate.day, 23, 59, 59)
	
	return 1 if nextSet < currentDate and currentDate <= toDate else 0

display()
print("---")
print("Next Sunset(" + getSunseTime().strftime("%x): %X"))
print("Moon Illumination: " + str(round(getIllumination(), 1)) + "%")
