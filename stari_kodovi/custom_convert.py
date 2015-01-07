#!/usr/bin/python
#
# skripta za konvertiranje među formatima
#
# stjepan.henc@fer.hr
#
# 22.05.2013
#

#LLS Lecture - Artificial Atmosphere

import sys, math

def procitaj_timecode(code):
	tmp = code.strip().split(":")
	
	#print("pro " + code)
	
	secs = 0
	
	for i in [0, 1, 2]:
		secs = secs*60 + int(tmp[i])
	
	# fakat cudni format, cini se da umjesto ms koristi 30-ti dio sekunde
	secs = secs + (int(tmp[3])*1000/30)/1000.0
	
	return secs

def generiraj_timecode(secs):

	h = math.floor(secs / 3600)
	
	secs %= 3600
	
	m = math.floor(secs / 60)
	
	secs %= 60
	
	s = math.floor(secs)
	
	secs -= s
	
	ms = round(secs * 1000)
	
	return str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2) + "," + str(ms).zfill(3)

fajl = open("./AA.txt", "r")

linije = fajl.readlines()

for i in range(0, len(linije)):
	if linije[i].strip():
		tmp = linije[i].partition(' ')
	
		tajming = tmp[0].strip().split(',')
	
		start = procitaj_timecode(tajming[0])
	
		end = procitaj_timecode(tajming[1])
	
		text = tmp[2].strip()
	
		print(i + 1)
		print(generiraj_timecode(start), "-->", generiraj_timecode(end))
		print(text + "\r\n")

