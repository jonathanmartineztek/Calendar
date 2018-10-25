#!/usr/bin/env python

import ephem #pip install pyephem
import datetime
import os
import urllib2

spottedAfter = 1

def onLine():
    try:
        urllib2.urlopen('http://www.google.com', timeout=1)
        return True
    except urllib2.URLError as err:
        return False

def readLog():
	inFile = open("log.txt")
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
	#input <type 'str'>
	if len(logB) == 2:
		inFile = open("log.txt", "a")
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
	#input <type 'datetime'>
	global yom
	yom = (datetime.date.today() - roshChodesh).days

def getNewMoon():
	global yyyymm
	#input <type 'str'>
	n = str(ephem.next_new_moon(yyyymm))
	# 2018/10/9 03:46:51
	n = n.split(" ")
	# ["2018/10/9", "03:46:51"]
	n = n[0].split("/")
	#["2018", "10", "9"]
	updateLog("/" + n[2])
	readLog()

	#return <type 'datetime.date'>
	return datetime.date(int(n[0]), int(n[1]), int(n[2])+spottedAfter)


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


#Python 2.7: https://repl.it/repls/ProudImmediateUser
#Python 3: https://repl.it/repls/RealFatLicensing
