#!/usr/bin/python
#
# stjepan.henc@fer.hr
# 05.02.2013
#
import wave, struct, math, sys, time

import matplotlib.pylab as pl

import scipy
import scipy.fftpack
import pylab
import scipy.stats
import numpy
#import pickle

import subtitle as s

audio = wave.open("data/901mali.wav", mode="r")

length = audio.getnframes()

sample_rate = audio.getframerate()

window = math.floor(sample_rate/50) # 20ms = 1s / 50
N = math.floor(length/window)

# metrics for every 20 ms
amplitude = pl.arange(0, N)
time = pl.arange(0, N)

postotak = 0

once = True

# read & preprocess the data from the file
for i in range(0, N):
	
	# get the 10 ms frame, merge the stereo channels
	frame = [0] * window
	for j in range(0, window):
		data = audio.readframes(1)
		#d = struct.unpack("<hh", data)
		d = struct.unpack("<h", data)
		frame[j] = d[0] #( int(d[0]) + int(d[1]) ) / 2

	
	
	# compute frame amplitude
	suma = 0	
	for j in range(0, window):	suma = suma + abs(frame[j])
	amplitude[i] = suma	/ window


#	#print(result)	
	postotak_novi = math.floor(i*100 / (length/window))
	
	if postotak_novi != postotak:
		postotak = postotak_novi
		sys.stdout.write("\b\b\b" + str(postotak) + "%")
		sys.stdout.flush()


audio.close()

# precomputed amplitude values
#str_amp = # ovdje ide string sa predcomputanim
#print(pickle.dumps(amplitude))
#amplitude = pickle.loads(str_amp)


# determine which frames to include and which not
included = pl.arange(0, N)
for i in range(0, N):
	if amplitude[i] > 500:
		included[i] = 1
	else:
		included[i] = 0

# same thing, just better
selected = pl.arange(0, N)
select = 0
brojac = 0

for i in range(0, N):
	if included[i] == 1:
		select = 1
		brojac = 25 # ako je tisina duza od 500 ms
	else:
		brojac -= 1

	if brojac == 0:
		select = 0

	selected[i] = select
	

# neuspjeli algoritam 1
#	broj = 0
#	lijevo = max(0, i - 5)
#	desno = min (i + 5, N)
#	c = desno - lijevo

#	for j in range(lijevo, desno):
#		if j != i and included[j] == 1:
#			broj += 1

#	if broj >  c/2 or included[i] == 1:
#		selected[i] = 1
#	else:
#		selected[i] = 0

## iscrtavanje rezultata
#			
pl.subplot(211)
pl.plot(time, amplitude)
#pl.subplot(312)
#pl.plot(time, included, 'ro')
pl.subplot(212)
pl.plot(time, selected, 'go')

#pl.show()

#time = pl.linspace(1, N, N)

#pl.subplot(311)
#pl.plot(time, energy)


# izbacivanje u .srt format

sub = s.SrtSubtitle()


# detektiraj pocetak, detektiraj kraj, pretvori u sekunde i dodaj titl
last = 0
start = 0
end = 0
for i in range(0, N):
	if last == 0 and selected[i] == 1:
		last = 1
		start = i * 0.02 # pretpostavka da frame traje 20ms
		continue
		
	if last == 1 and selected[i] == 0:
		last = 0
		end = (i + 1) * 0.02
		# start i end moraju biti u sekundama
		tmp = s.SubtitleLine(start, end)
		sub.add_subs(tmp)


sub.serialize('data/901mali.srt')
