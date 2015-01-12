#!/usr/bin/python3

import numpy as np # no problem
import librosa as lbr 
import matplotlib.pyplot as plt

import time

from a_weighting import itu_r_468_amplitude_weight

from detect_speech import detect_speech


def weighted_mixer(y1, y2, sr, intervals, nmels, hopl):
""" """
if __name__ == "__main__":	
	snr = -3

	y1, sr = lbr.load('speech.wav', 16000)
	y2, sr = lbr.load('noise.wav', 16000) # have to guess samplerate, otherwise the code might hang

	intervals = detect_speech(y1, sr, hopl)

	nmels = 128
	hopl = 64
	# compute mel spectrogram
	S1 = lbr.feature.melspectrogram(y1, sr=sr, n_fft=2048, hop_length=hopl, n_mels=nmels)
	S2 = lbr.feature.melspectrogram(y2, sr=sr, n_fft=2048, hop_length=hopl, n_mels=nmels)

	# get frequencies for bins
	mel_freqs = lbr.mel_frequencies(n_mels=nmels, fmin=0, fmax=sr/2)

	itu_r_468 = itu_r_468_amplitude_weight()

	log_aw = np.array(itu_r_468(mel_freqs))

	log_S1 = lbr.logamplitude(S1, ref_power=np.max) + log_aw[:, np.newaxis]
	log_S2 = lbr.logamplitude(S2, ref_power=np.max) + log_aw[:, np.newaxis]

	##lbr.display.specshow(log_S1, sr=sr, hop_length=64, x_axis='time', y_axis='mel')
	#lbr.display.specshow(log_S1, sr=sr, hop_length=64, x_axis='time', y_axis='mel')
	##lbr.display.specshow(S1/np.max(S1), sr=sr, hop_length=64, x_axis='time', y_axis='mel')

	#plt.title('mel power spectrogram')

	##plt.colorbar(format='%+02.0f dB')

	#plt.tight_layout()

	#plt.show()

	##time.sleep(2000)
	#alog_S1 = log_S1 + log_aw[:,np.newaxis]

	#lbr.display.specshow(alog_S1, sr=sr, hop_length=64, x_axis='time', y_axis='mel')

	#plt.title('mel power spectrogram itu-r 468')

	#plt.tight_layout()

	#plt.show()
