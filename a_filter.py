#!/usr/bin/python3
# stjepan.henc@fer.hr

import numpy as np # no problem
import librosa as lbr 
import matplotlib.pyplot as plt
from scipy.signal import lfilter, freqz

import math

from a_weighting2 import itu_r_468_amplitude_weight

from detect_speech import detect_speech

from parseval_functions import rms_flat, rms_fft

def a_filter(y, sr, intervals, mode=0):
	snr = 0
	
	itur468 = itu_r_468_amplitude_weight()
	
	#print(intervals)
	
	if mode == 1:
	
	#	tmp = math.sqrt(np.average(y*y))
		
	#	print(tmp)
		
	#	print(rms_flat(y))
		snr = 20 * math.log10(rms_flat(y))
	
	elif mode == 0: 
		
		tmpylen = sum([ i[1] - i[0] for i in intervals])
		
		#print(tmpylen)
		tmp = np.zeros(tmpylen)
		
		pos = 0
		for i in intervals:
			
			diff = i[1] - i[0]
			
			tmp[pos : pos + diff] = y[ i[0]:i[1] ]
			
			pos = pos + diff
		
		S = lbr.stft(y, n_fft=2048, hop_length=64)
		
		fr = lbr.fft_frequencies(sr, n_fft=2048)
		
		gains = itur468(fr)
		
		sh = S.shape[1]
		n = S.shape[0]
		
		avgs = np.zeros(sh)
		
		# parseval equation to avoid iSTFT
		
		for i in range(sh):
			S[:, i] = S[:, i] * gains
			#avgs[i] = math.sqrt( sum(abs(S[:, i] * S[:, i]) / (n**2)) )
			#print (avgs[i])
			#print (rms_fft(S[:,i]))
			avgs[i] = rms_fft(S[:,i])
		
		# final average magnitude

		avg = np.average(avgs)
		
	#	plt.subplot(211)
	#	plt.plot(np.arange(len(y)), y)
	#	plt.subplot(212)
	#	plt.plot(np.arange(len(tmp)), tmp)	
	#	plt.show()
		
	#	plt.plot(fr, gains)	
	#	plt.show()
		
		snr = 20 * math.log10( avg )
	
	elif mode == 2: 
		
		tmpylen = sum([ i[1] - i[0] for i in intervals])
		
		print(tmpylen)
		tmp = np.zeros(tmpylen)
		
		pos = 0
		for i in intervals:
			
			diff = i[1] - i[0]
			
			tmp[pos : pos + diff] = y[ i[0]:i[1] ]
			
			pos = pos + diff
			
	#	plt.subplot(211)
	#	plt.plot(np.arange(len(y)), y)
	#	plt.subplot(212)
	#	plt.plot(np.arange(len(tmp)), tmp)	
	#	plt.show()
		
		snr = 20 * math.log10( rms_flat(tmp) )
	
	else:
		snr = 0
	

	return snr

if __name__ == "__main__":
	
	y, sr = lbr.load('noise_lf.wav', 16000)
	
	nmels = 128
	hopl = 64
	
	intervals = detect_speech(y, sr, mode=1)

	print("SNR (without A_weighting) = ", a_filter(y, sr, intervals, mode = 1))
	
	print("SNR (with A_weighting)    = ", a_filter(y, sr, intervals, mode = 0))
