#!/usr/bin/python3

import numpy as np # no problem
import librosa as lbr 
import matplotlib.pyplot as plt
from scipy.signal import lfilter, freqz

import time

from a_weighting2 import itu_r_468_amplitude_weight_dB

from A_weighting import A_weighting

from detect_speech import detect_speech

from a_filter import a_filter

def compute_gain(y1, y2, sr, des_snr, intervals, AW):
	
	if AW == True:
		print("Using A weighting")
		snr1 = a_filter(y1, sr, intervals, mode=0) # use A weighting mode
		snr2 = a_filter(y2, sr, intervals, mode=0) 
	else:
		print("Not using A weighting")
		snr1 = a_filter(y1, sr, intervals, mode=1)
		snr2 = a_filter(y2, sr, intervals, mode=1) # don't use weighting
		
	print("Applying gain for %.2f dB" % (snr2 - snr1 - des_snr))

	gain = 10**((snr2 - snr1 - des_snr)/20) # from amplitude dB to gain

	return gain

def weighted_mixer(y1, y2, sr, nmels, hopl, des_snr, AW=True):
	"""Mix speech with the noise at the specified SNR
	
	Args:
		y1 - speech signal
		y2 - noise/music
		sr - samplerate
		nmels - number of mel bins
		hopl - hop lenght
		des_snr - desired SNR of speech to noise
		
	Returns:
	
		np.array containing 16-bit resolution sound samples 
	
	Note:
		doesn't work with stereo yet
	"""

	intervals = detect_speech(y1, sr, hopl, mode=1)

	gain = compute_gain(y1, y2, sr, des_snr, intervals, AW)
	
	len_ret = min(len(y1), len(y2))
	
	y_ret = y1[0:len_ret] + gain * y2[0:len_ret] 
	
	return y_ret
	
def weighted_mixer_stereo(y1, y2, sr, nmels, hopl, des_snr, AW=True):
	"""Mix speech with the noise at the specified SNR
	
	Args:
		y1 - speech signal
		y2 - noise/music
		sr - samplerate
		nmels - number of mel bins
		hopl - hop lenght
		des_snr - desired SNR of speech to noise
		
	Returns:
	
		np.array containing 16-bit resolution sound samples 
	
	Note:
		doesn't work with stereo yet
	"""
	y1 = y1.T
	y2 = y2.T

	intervals = detect_speech(y1, sr, hopl, mode=1)

	y1m = (y1[:, 0] + y1[:,1]) / 2
	y2m = (y2[:, 0] + y2[:,1]) / 2

	gain = compute_gain(y1m, y2m, sr, des_snr, intervals, AW)
	
	len_ret = min(len(y1), len(y2))
	
	y_ret = y1[0:len_ret] + gain * y2[0:len_ret] 
	
	return y_ret.T

def show_spectrogram(y, sr, n_fft, nmels, hopl, AW=False):


	
	S = lbr.feature.melspectrogram(y, sr=sr, n_fft=2048, hop_length=hopl, n_mels=nmels)
	
	log_S = lbr.logamplitude(S, ref_power=np.max)

	if AW:
			
		# get frequencies for bins	
		mel_freqs = lbr.mel_frequencies(n_mels=nmels, fmin=0, fmax=sr/2)

		itu_r_468 = itu_r_468_amplitude_weight_dB()

		# compute a_weighting coefficient for every bin
		log_aw = np.array(itu_r_468(mel_freqs))
		
		log_S = log_S + log_aw[:, np.newaxis]
	
	lbr.display.specshow(log_S, sr=sr, hop_length=64, x_axis='time', y_axis='mel')
	
	plt.title('mel power spectrogram')
	
	plt.tight_layout()
	
	plt.show()

	return log_S
	
if __name__ == "__main__":	
	snr = -3

#	y1, sr = lbr.load('speech.wav', 16000)
#	y2, sr = lbr.load('noise_lf.wav', 16000) # have to guess samplerate, otherwise the code might hang
	
	y1, sr = lbr.load('speech.wav', mono=False, sr=16000)
	y2, sr = lbr.load('noise_lf.wav', mono=False, sr=16000)
	
	nmels = 128
	hopl = 64
	
#	y_out = weighted_mixer(y1, y2, sr, nmels, hopl, -9, AW=True)
	
	y_out = weighted_mixer_stereo(y1, y2, sr, nmels, hopl, -9, AW=True)
	
	lbr.output.write_wav('output.wav', y_out.T, sr, normalize=True) # hm ... normalization || !normalization ?
		
	#show_spectrogram(y1, sr, 2048, nmels, hopl)
	#show_spectrogram(y2, sr, 2048, nmels, hopl)
	#show_spectrogram(y_out, sr, 2048, nmels, hopl)


	y_out = weighted_mixer(y1, y2, sr, nmels, hopl, -9, AW=False)
	
	lbr.output.write_wav('output_NA.wav', y_out.T, sr, normalize=True) # hm ... normalization || !normalization ?
		
	#show_spectrogram(y1, sr, 2048, nmels, hopl)
	#show_spectrogram(y2, sr, 2048, nmels, hopl)
	#show_spectrogram(y_out, sr, 2048, nmels, hopl)
