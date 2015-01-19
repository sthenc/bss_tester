#!/usr/bin/python3

import numpy as np # no problem
import librosa as lbr 
import matplotlib.pyplot as plt

from detect_speech import detect_speech

from subtitle import SrtSubtitle, Subtitle, SubtitleLine

# maximum and minimum durations
durmax = 90
durmin = 70

def connect_subs(titlovi):
	ret = []
	
	tmpbeg = -1
	tmpend = -1
	tmptext = ""
	
	# unnecessary
	#tmpfin = titlovi[-1].end	
	
	#durtot = tmpfin - tmpbeg
	
	for i in range(0, len(titlovi)):
				
		tmpend = titlovi[i].end
		tmptext = tmptext + '\n' + titlovi[i].text.strip()

		if tmpbeg == -1:
			tmpbeg = titlovi[i].start
			tmptext = tmptext.strip()
		
		if tmpend - tmpbeg > durmin:
			
			ret.append([tmpbeg, tmpbeg + min(tmpend-tmpbeg, durmax), tmptext])
			tmpbeg = -1
			tmpend = -1
			tmptext = ""
		
	# we will loose some data on the end, but we don't care, it's less than durmin
	
	return ret

def cut_audio(y, sr, start, end):
	start = max(start * sr, 0)
	end = min(end * sr, len(y))

	return y[start:end]

input_folder = '/mnt/data/Fer/diplomski/test_data3/unsegmented/'

input_names = [ '%02d' % i for i in range(1, 11)]
#input_wavs = '01.wav'
#input_srts = '01.srt'

N_out = 1
output_folder_wav = '/mnt/data/Fer/diplomski/test_data3/clean_speech/'
output_folder_srt = '/mnt/data/Fer/diplomski/test_data3/transcripts/'

for name in input_names:

	input_srt = input_folder + name + '.srt'
	input_wav = input_folder + name + '.wav'

	s = SrtSubtitle()

	s.deserialize(input_srt)

	titlovi = s.get_subs()

	transkripti = connect_subs(titlovi)

	#print(transkripti)

	y, sr = lbr.load(input_wav, mono=False, sr=16000)
	
	y = y.T

	for i in range(len(transkripti)):
		
		y_out = cut_audio(y,sr, transkripti[i][0], transkripti[i][1])
		
		lbr.output.write_wav(output_folder_wav + '%03d.wav' % N_out, y_out, sr, normalize=True)
		
		f = open(output_folder_srt + '%03d.txt' % N_out, 'w')
		
		f.write(transkripti[i][2])
		
		f.close()
		
		print("Generated %d file" % N_out)
		
		N_out += 1
		
