
#!/usr/bin/python3

import numpy as np # no problem
import librosa as lbr 
import matplotlib.pyplot as plt


# maximum and minimum durations
durmax = 90

def cut_audio(y, sr, start, end):
	start = max(start * sr, 0)
	end = min(end * sr, len(y))

	return y[start:end]

input_folder = '/mnt/data/Fer/diplomski/test_data3/unsegmented_noise/'

input_names = ['01'] #[ '%02d' % i for i in range(1, 11)]
#input_wavs = '01.wav'
#input_srts = '01.srt'

N_out = 1
output_folder_wav = '/mnt/data/Fer/diplomski/test_data3/noise/'

for name in input_names:

	input_wav = input_folder + name + '.wav'


	#print(transkripti)

	y, sr = lbr.load(input_wav, mono=False, sr=16000)
	
	y = y.T

	pos = 0
	for i in range(50):
		
		y_out = cut_audio(y,sr, pos, pos + durmax)
		
		pos += durmax
		
		lbr.output.write_wav(output_folder_wav + '%03d.wav' % N_out, y_out, sr, normalize=True)
		
		print("Generated %d file" % N_out)
		
		N_out += 1
		
