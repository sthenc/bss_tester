#!/usr/bin/python3
import numpy as np # no problem
import librosa as lbr 
import matplotlib.pyplot as plt
import math

def detect_speech(y, sr, window=-1): # window = mel_bins /2 because of 50% overlap

	#segment signal into frames of approx 10 ms
	if window==-1:
		window = sr / 100 # samples in 10 ms
	
	N = math.ceil(len(y) / window)
	
	data = np.array(y).resize(N, window)

	amplitude = np.zeros(N)
	
	for i in range(0, N):
		amplitude[i] = sum(abs(data(i, :))) / window
		
	avgamp = sum(amplitude) / N

	treshold = avgamp * 0.1

	# determine which frames to include and which not
	included = np.zeros(N)
	for i in range(0, N):
		if amplitude[i] > treshold:
			included[i] = 1
		else:
			included[i] = 0

	# same thing, just better
	selected = np.zeros(N)
	select = 0
	brojac = 0

	for i in range(0, N):
		if included[i] == 1:
			select = 1
			brojac = 50 # ako je tisina duza od 500 ms
		else:
			brojac -= 1

		if brojac == 0:
			select = 0

		selected[i] = select
		
	return selected

if __name__ == "__main__":		
	y1, sr = lbr.load('speech.wav', 16000)
	
	
