#!/usr/bin/python3
# stjepan.henc@fer.hr

import numpy as np # no problem
import librosa as lbr 
import matplotlib.pyplot as plt
from scipy.signal import lfilter, freqz

import math

from a_weighting2 import itu_r_468_amplitude_weight

def a_filter(y, sr, intervals, mode=0):
	snr = 0
	
	itur468 = itu_r_468_amplitude_weight
	
	print(intervals)
	
	if mode == 1:
	
		tmp = np.average(abs(y))
		
		snr = 20 * math.log10(tmp)
	
	elif mode == 0: 
		
		tmp = 2
		snr = -1
		
	else:
		snr = 0
	

	return snr

if __name__ == "__main__":
	
		print("hello")
