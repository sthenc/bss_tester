#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# stjepan.henc@fer.hr
# 05.02.2013
#

import math

class SubtitleLine:
	def __init__(self, start, end, text = '\n'):
		self.start = float(start)
		self.end = float(end)
		self.text = text

	def __str__(self):
		return "" + str(self.start) + "," + str(self.end) + "," + self.text

class Subtitle:
	"""Abstract subtitle class"""	

	def __str__(self):
		raise NotImplementedError("Abstract __str__")
	
	def serialize(self, filename):
		raise NotImplementedError("Abstract serialize")
	
	def deserialize(self, filename):
		raise NotImplementedError("Abstract deserialize")
		
	def get_subs(self, ):
		return self.subs

	def add_subs(self, sub):
		self.subs.append(sub)
	#TODO mozda vise varijanti funkcije

#class AssSubtitle(Subtitle):
#	"""Class for serializing and deserializing .ASS subtitles
#	self.header - stored header from last read subtitle
#	self.subtitles - array of SubtitleLine objects

#	serialize(filename) - store subtitles to .ass file, destroys styling info
#	deserialize(filename) - load subtitles form .ass, destroys styling info"""
#	
#	def __init__(self):
#		self.header = """
#﻿[Script Info]
#Title: Default Aegisub file
#ScriptType: v4.00+
#WrapStyle: 0
#PlayResX: 640
#PlayResY: 480
#ScaledBorderAndShadow: yes
#Video Aspect Ratio: 0
#Video Zoom: 6
#Video Position: 0
#Audio File: small.wav

#[V4+ Styles]
#Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
#Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1
#"""
#		#self.header = self.header.encode("utf-8")

#	def __str__(self):
#		return "=" * 40 + self.header + "=" * 40

#	def serialize(self, filename):
#		fajl = open(filename, "w")
#	
#		for i in range(0, len(self.subs)):
#			fajl.write(str(i + 1) + "\n")
#			fajl.write(self.generiraj_timecode(self.subs[i].start) + " --> " + self.generiraj_timecode(self.subs[i].end) + "\n")
#			#fajl.write(str(self.subs[i].start) + " --> " + str(self.subs[i].end) + "\n")
#			fajl.write(self.subs[i].text) # text ima jedan newline viska
#		
#		fajl.close()		
#	
#	def deserialize(self, filename):
#		fajl = open(filename, "r")

#		# ass format:
#		#   broj linije
#		#   timecode --> timecode
#		#   text
#		#   text
#		#   prazna linija
#		
#		linije = fajl.readlines()
#		linije.append("\n") # algoritam pretpostavlja da titl zavrsava s praznom linijom
#		bafer = []
#		
#		for i in range(0, len(linije)):
#			if not linije[i].strip():
#				tajming = bafer[1].strip().split(' ')
#	
#				start = self.procitaj_timecode(tajming[0])
#	
#				end = self.procitaj_timecode(tajming[2])

#				text = ""
#				for j in range(2, len(bafer)):
#					text += bafer[j] + "\n"
#				
#				self.subs.append(SubtitleLine(start, end, text))
#				bafer = []

#			if linije[i].strip():
#				bafer.append(linije[i])

class SrtSubtitle(Subtitle):
	""".srt subtitle class i/o"""
	
	def __init__(self):
		self.subs = []
		
	def __str__(self):

		return str(self.subs[i].start) + " --> " + str(self.subs[i].end) + "\n" + self.subs[i].text
			
	def procitaj_timecode(self, code):
		tmp = code.strip().split(":")
	
		#print("pro " + code)
	
		secs = 0
	
		for i in [0, 1, 2]:
			secs = secs*60 + float(tmp[i].replace(",","."))
	
		return secs

	def generiraj_timecode(self, secs):

		h = math.floor(secs / 3600)
	
		secs %= 3600
	
		m = math.floor(secs / 60)
	
		secs %= 60
	
		s = math.floor(secs)
	
		secs -= s
	
		ms = round(secs * 1000)
	
		return str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2) + "," + str(ms).zfill(3)	

	def serialize(self, filename):
		fajl = open(filename, "w")
	
		for i in range(0, len(self.subs)):
			fajl.write(str(i + 1) + "\n")
			fajl.write(self.generiraj_timecode(self.subs[i].start) + " --> " + self.generiraj_timecode(self.subs[i].end) + "\n")
			#fajl.write(str(self.subs[i].start) + " --> " + str(self.subs[i].end) + "\n")
			fajl.write(self.subs[i].text) # text ima jedan newline viska
		
		fajl.close()		
	
	def deserialize(self, filename):
		fajl = open(filename, "r")

		# srt format:
		#   broj linije
		#   timecode --> timecode
		#   text
		#   text
		#   prazna linija
		
		linije = fajl.readlines()
		linije.append("\n") # algoritam pretpostavlja da titl zavrsava s praznom linijom
		bafer = []
		
		for i in range(0, len(linije)):
			if not linije[i].strip():
				tajming = bafer[1].strip().split(' ')
	
				start = self.procitaj_timecode(tajming[0])
	
				end = self.procitaj_timecode(tajming[2])

				text = ""
				for j in range(2, len(bafer)):
					text += bafer[j] + "\n"
				
				self.subs.append(SubtitleLine(start, end, text))
				bafer = []

			if linije[i].strip():
				bafer.append(linije[i])
				
	
if __name__ == "__main__":

	s = SrtSubtitle()
	s.deserialize("./data/small.srt")

	s.serialize("./data/test_small.srt")

	#print(s.generiraj_timecode(s.procitaj_timecode("01:12:31,830")))
