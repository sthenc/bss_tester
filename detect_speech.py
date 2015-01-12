#!/usr/bin/python3
import numpy as np # no problem
import librosa as lbr 
import matplotlib.pyplot as plt
import math

# works only on very clean speech like audiobooks
# returns list of tuples (#begining window, #ending window)
def detect_speech(y, sr, window=-1): # window = mel_bins /2 because of 50% overlap

	#segment signal into frames of approx 10 ms
	if window==-1:
		window = sr / 100 # samples in 10 ms
	
#	print(y, sr, window)
	
	N = math.ceil(len(y) / window)
	
	data = np.resize(np.array(y), (N, window))

#	print(N, data)
	
	amplitude = np.zeros(N)
	
	for i in range(0, N):
		amplitude[i] = sum(abs(data[i])) / window
		
	avgamp = sum(amplitude) / N

	treshold = avgamp * 0.57

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

	intervals = []
	
	start = 0
	end = 0
	brojac = 0
	
	for i in range(0, N):
		if selected[i] == 1:
			if brojac == 0:
				start = i
				brojac = 1
		else:
			if brojac == 1:		
				end = i
				tmp = (start*1.0, end*1.0)
				intervals.append(tmp)
				brojac = 0
			
	return intervals

if __name__ == "__main__":		
	y1, sr = lbr.load('speech.wav', 16000)
	#y1, sr = lbr.load('speech_long.wav', 16000)
	#y1, sr = lbr.load('speech_bad2.wav', 16000)
	
	intervals = detect_speech(y1, sr, 64)
	
	print(intervals)
	
	S1 = lbr.feature.melspectrogram(y1, sr=sr, n_fft=2048, hop_length=64, n_mels=128)
	
	log_S1 = lbr.logamplitude(S1, ref_power=np.max)
	
	plt.figure(1)
	plt.title('mel power spectrogram itu-r 468')
	plt.subplot(211)
	
	lbr.display.specshow(log_S1, sr=sr, hop_length=64, x_axis='time', y_axis='mel')
	
	for i in intervals:
		plt.axhspan(0, 5, i[0]*64.0/len(y1), i[1]*64.0/len(y1), color='green')
	
	plt.subplot(212)
	
	plt.plot(range(len(y1)), y1)
	
	#plt.subplot(313)
	#plt.plot(range(len(intervals)), intervals)

	plt.tight_layout()

	plt.show()

