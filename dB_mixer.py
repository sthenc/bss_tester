#!/usr/bin/python3

import numpy as np # no problem
import librosa as lbr 
import matplotlib.pyplot as plt

from weighted_mixer import weighted_mixer_stereo

speech_folder = '/mnt/data/Fer/diplomski/test_data3/clean_speech/'

noise_folder = '/mnt/data/Fer/diplomski/test_data3/noise/'

snrs = [-6, 0, 6, 20] #not enough time [20 10 6 3 0 -3 -6]

output_root = '/mnt/data/Fer/diplomski/test_data3/'

output_folders = ['mix_m6dB', 'mix_0dB', 'mix_6dB', 'mix_20dB']

filenames = ["%03d" % i for i in range(1,6)]

nmels = 128
hopl = 64

for f in filenames:
	
	y1, sr = lbr.load(speech_folder + f + '.wav', mono=False, sr=16000)
	y2, sr = lbr.load(noise_folder + f + '.wav', mono=False, sr=16000)
	
	for i in range(len(snrs)):
		y_out = weighted_mixer_stereo(y1, y2, sr, nmels, hopl, snrs[i], AW=True)
		
		lbr.output.write_wav(output_root + output_folders[i] + '/' + f + '.wav', y_out.T, sr, normalize=True)

