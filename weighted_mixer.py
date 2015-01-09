#!/usr/bin/python3

import numpy as np # no problem
import librosa as lbr 
import matplotlib.pyplot as plt

import time

from a_weighting import itu_r_468_amplitude_weight

snr = -3

y1, sr = lbr.load('speech.wav', 16000)
y2, sr = lbr.load('noise.wav', 16000) # have to guess samplerate, otherwise the code might hang

# compute mel spectrogram
S1 = lbr.feature.melspectrogram(y1, sr=sr, n_fft=2048, hop_length=64, n_mels=128)
S2 = lbr.feature.melspectrogram(y2, sr=sr, n_fft=2048, hop_length=64, n_mels=128)

log_S1 = lbr.logamplitude(S1, ref_power=np.max)

mel_freqs = lbr.mel_frequencies(n_mels=128, fmin=0, fmax=sr/2)

itu_r_468 = itu_r_468_amplitude_weight()

log_aw = np.array(itu_r_468(mel_freqs))
# get frequencies for bins

#plt.figure(figsize=(12,4))

#lbr.display.specshow(log_S1, sr=sr, hop_length=64, x_axis='time', y_axis='mel')
lbr.display.specshow(log_S1, sr=sr, hop_length=64, x_axis='time', y_axis='mel')
#lbr.display.specshow(S1/np.max(S1), sr=sr, hop_length=64, x_axis='time', y_axis='mel')


plt.title('mel power spectrogram')

#plt.colorbar(format='%+02.0f dB')

plt.tight_layout()

plt.show()

#time.sleep(2000)
alog_S1 = log_S1 + log_aw[:,np.newaxis]

lbr.display.specshow(alog_S1, sr=sr, hop_length=64, x_axis='time', y_axis='mel')

plt.title('mel power spectrogram itu-r 468')

plt.tight_layout()

plt.show()
