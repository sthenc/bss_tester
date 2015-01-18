#!/usr/bin/python3
# stjepan.henc@fer.hr

import numpy as np # no problem
import librosa as lbr 
import matplotlib.pyplot as plt
from scipy.signal import lfilter, freqz

import math

from a_weighting2 import itu_r_468_amplitude_weight

from detect_speech import detect_speech

def a_filter(y, sr, intervals, mode=0):
	snr = 0
	
	itur468 = itu_r_468_amplitude_weight
	
	print(intervals)
	
	if mode == 1:
	
		tmp = np.average(abs(y))
		
		print(tmp)
		snr = 20 * math.log10(tmp)
	
	elif mode == 0: 
		
		tmpylen = sum([ i[1] - i[0] for i in intervals])
		
		print(tmpylen)
		tmp = np.zeros(tmpylen)
		
		snr = -1
		
	else:
		snr = 0
	

	return snr

if __name__ == "__main__":
	
	y, sr = lbr.load('speech.wav', 16000)
	
	nmels = 128
	hopl = 64
	
	intervals = detect_speech(y, sr, hopl, mode=1)

	print("SNR (without A_weighting) = ", a_filter(y, sr, intervals, mode = 1))
	
	print("SNR (with A_weighting)    = ", a_filter(y, sr, intervals, mode = 0))
