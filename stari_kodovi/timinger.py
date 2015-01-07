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



audio = wave.open("data/small.wav", mode="r")

length = audio.getnframes()

sample_rate = audio.getframerate()

total_suma = 0
total_min = 64000
total_max = -1

window = math.floor(sample_rate/100)
N = math.floor(length/window)

# metrics for every 10 ms
energy = [0] * N
max_freq = [0] * N
spectral_flatness = [0] * N

postotak = 0

once = True

# read & preprocess the data from the file
for i in range(0, N):
	
	# get the 10 ms frame, merge the stereo channels
	frame = [0] * window
	for j in range(0, window):
		data = audio.readframes(1)
		d = struct.unpack("<hh", data)
		frame[j] = ( int(d[0]) + int(d[1]) ) / 2
	
	# compute frame energy
	suma = 0	
	for j in range(0, window):	suma = suma + frame[j]**2
	energy[i] = suma
	
	# compute frame fft
	
	frame_fft = abs(abs(scipy.fft(frame)))
	
	# compute SFM - Spectral Flatness Measure
	# arithmetic mean of spectrum
	Am = numpy.mean(frame_fft)
	
	# geometric mean of spectrum
	Gm = scipy.stats.gmean(frame_fft)
	
	if once:
		print(Gm, Am)
		once = False
	
	spectral_flatness[i] = 10 * math.log10(Gm / Am)
	
	# compute the frequency with the greatest amplitude
	freqs = scipy.fftpack.fftfreq(window, 0.0001)
	max_freq[i] = 0
	maximum = -1
	max_pos = 0
	for j in range(0, window):
		if (frame_fft[j] > maximum):
			maximum = frame_fft[j]
			max_pos = j
			
	max_freq[i] = freqs[max_pos]
	#print(result)	
	postotak_novi = math.floor(i*100 / (length/window))
	
	if postotak_novi != postotak:
		postotak = postotak_novi
		sys.stdout.write("\b\b\b" + str(postotak) + "%")
		sys.stdout.flush()

audio.close()

time = pl.linspace(1, N, N)

pl.subplot(311)
pl.plot(time, energy)
pl.subplot(312)
pl.plot(time, max_freq)
pl.subplot(313)
pl.plot(time, spectral_flatness)

pl.show()

#print()

#total_avg = total_suma/length

#print(total_min, total_max, total_avg, N)

## find the silences 

#silence = False

#points = []

#for i in range(0, N):
#	if !silence:
#				
#	
#	
#	else:



# outfile ... 
