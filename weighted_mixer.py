#!/usr/bin/python3

import numpy as np # no problem
import librosa as lbr 
import matplotlib.pyplot as plt
from scipy.signal import lfilter

import time

from a_weighting2 import itu_r_468_amplitude_weight

from A_weighting import A_weighting

from detect_speech import detect_speech


def weighted_mixer(y1, y2, sr, nmels, hopl):
	"""Mix speech with the noise at the specified SNR
	
	Args:
		y1 - speech signal
		y2 - noise/music
		sr - samplerate
		nmels - number of mel bins
		hopl - hop lenght
		
	Returns:
	
		np.array containing 16-bit resolution sound samples 
	
	Note:
		doesn't work with stereo yet
	"""

	intervals = detect_speech(y1, sr, hopl)

	# compute mel spectrogram
	S1 = lbr.feature.melspectrogram(y1, sr=sr, n_fft=2048, hop_length=hopl, n_mels=nmels)
	S2 = lbr.feature.melspectrogram(y2, sr=sr, n_fft=2048, hop_length=hopl, n_mels=nmels)

	# get frequencies for bins	
	mel_freqs = lbr.mel_frequencies(n_mels=nmels, fmin=0, fmax=sr/2)

	itu_r_468 = itu_r_468_amplitude_weight()

	# compute a_weighting coefficient for every bin
	log_aw = np.array(itu_r_468(mel_freqs))

	# compute logarithm of amplitude and apply itu-r 468 a_weighting
	log_S1 = lbr.logamplitude(S1, ref_power=np.max) + log_aw[:, np.newaxis]
	log_S2 = lbr.logamplitude(S2, ref_power=np.max) + log_aw[:, np.newaxis]

	#log_SA1 = np.average(log_S1, axis=2, )

	gain = 0.5
	
	len_ret = min(len(y1), len(y2))
	
	y_ret = y1[0:len_ret] + gain * y2[0:len_ret] 
	
	return y_ret

def show_spectrogram(y, sr, n_fft, nmels, hopl, AW=False):


	
	S = lbr.feature.melspectrogram(y, sr=sr, n_fft=2048, hop_length=hopl, n_mels=nmels)
	
	log_S = lbr.logamplitude(S, ref_power=np.max)

	if AW:
			
		# get frequencies for bins	
		mel_freqs = lbr.mel_frequencies(n_mels=nmels, fmin=0, fmax=sr/2)

		itu_r_468 = itu_r_468_amplitude_weight()

		# compute a_weighting coefficient for every bin
		log_aw = np.array(itu_r_468(mel_freqs))
		
		log_S = log_S + log_aw[:, np.newaxis]
	
	lbr.display.specshow(log_S, sr=sr, hop_length=64, x_axis='time', y_axis='mel')
	
	plt.title('mel power spectrogram')
	
	plt.tight_layout()
	
	plt.show()

if __name__ == "__main__":	
	snr = -3

	y1, sr = lbr.load('speech.wav', 16000)
	y2, sr = lbr.load('noise.wav', 16000) # have to guess samplerate, otherwise the code might hang
	
	nmels = 128
	hopl = 64
	
	y_out = weighted_mixer(y1, y2, sr, nmels, hopl)
	
	b, a = A_weighting(sr)
	
	y_out2 = lfilter(b, a, y_out) 
	
	#show_spectrogram(y1, sr, 2048, nmels, hopl)
	#show_spectrogram(y2, sr, 2048, nmels, hopl)
	#show_spectrogram(y_out, sr, 2048, nmels, hopl)
	#show_spectrogram(y_out, sr, 2048, nmels, hopl, AW=True)
	#show_spectrogram(y_out2, sr, 2048, nmels, hopl)
	
	print (y_out)
	lbr.output.write_wav('output.wav', y_out, sr, normalize=True) # hm ... normalization || !normalization ?
	
	
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
