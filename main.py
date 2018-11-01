#!/usr/bin/env python

#https://repl.it/@jonathanmartinez/FussyHuskyProgram

import ephem #pip install pyephem
import datetime
import os
from pytz import timezone
import urllib2

nowPacific = datetime.datetime.now(timezone("US/Pacific"))
nowUTC = datetime.datetime.utcnow().strftime("%Y/%m/%d")
nextUTC = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).strftime("%Y/%m/%d")
spottedAfter = 1

def obServer():
	home = ephem.Observer()
	home.lat = "33.98"
	home.lon = "-117.37"
	home.elevation = 260
	#To get U.S. Naval Astronomical Almanac values, use these settings
	home.pressure = 0
	home.horizon = "-0:34"

	return home

def readLog():
	global log

	log = os.path.expanduser('~') + "/Documents/log.txt"
	inFile = open(log)
	try:
		global chodesh
		global yyyymm
		global year
		global month
		global day
		global logB
		global yom
		global disPlay

		content = inFile.readlines()
		log = content[len(content)-1].split(";")

		chodesh = getChodesh(log[0])
		yyyymm = log[1]

		logB = log[1].split("/")
		year = int(logB[0])
		month = int(logB[1])
		if len(logB) == 2:
			getNewMoon()
		elif len(logB) == 3:
			disPlay = True
			day = int(logB[2])
			roshChodesh = datetime.date(year, month, day+spottedAfter)
			daySince(roshChodesh)
			if isNowInTimePeriod():
				if yom == 29 or yom == 30:
					if getIllumination() >= 1.5:
						updateLog("\n" + str(int(log[0])+1) + ";" + str(nowUTC.year) + "/" + str(nowUTC.month))
						getNewMoon()

	finally:
		inFile.close()

def updateLog(update):
	if len(logB) == 2 or "\n" in update:
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

def daySince(roshChodesh):
	global yom

	to_day = datetime.date(nowPacific.year,nowPacific.month, nowPacific.day)
	yom = (to_day - roshChodesh).days + isNowInTimePeriod()

def getNewMoon():
	global yyyymm

	n = str(ephem.next_new_moon(yyyymm)).split(" ")
	# ["2018/10/9", "03:46:51"]
	n = n[0].split("/")
	#["2018", "10", "9"]
	updateLog("/" + n[2])
	readLog()

	#return <type 'datetime.date'>
	return datetime.date(int(n[0]), int(n[1]), int(n[2]) + spottedAfter)

def getIllumination():
	moon = ephem.Moon()
	moon.compute(obServer())

	return round(float(moon.moon_phase * 100),1)

def getSunseTime(date):
	global sunseTime

	home = obServer()
	home.date = date
	sun = ephem.Sun()
	sun.compute(home)
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
	nowSet = getSunseTime(nowUTC)
	toDate = nowPacific.replace(nowPacific.year,nowPacific.month, nowPacific.day, 23, 59, 59)

	return 1 if nowSet < nowPacific and nowPacific <= toDate else 0

def onLine():
	try:
		urllib2.urlopen('http://www.google.com', timeout=1)
		return True
	except urllib2.URLError as err:
		return False

def display():
	readLog()
	if onLine() and disPlay:
			print(chodesh + " " + str(yom))
	elif not onLine() and disPlay:
			print(chodesh + " " + str(yom) + "*")

display()
print("---")
print("Moon Illumination: " + str(getIllumination()) + "%")
if getSunseTime(nowUTC) <= nowPacific:
	 print("Next Sunset(" + getSunseTime(nextUTC).strftime("%x): %X"))
else:
	print("Next Sunset(" + getSunseTime(nowUTC).strftime("%x): %X"))
