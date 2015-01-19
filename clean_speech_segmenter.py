#!/usr/bin/python3

import numpy as np # no problem
import librosa as lbr 
import matplotlib.pyplot as plt

from detect_speech import detect_speech

from subtitle import SrtSubtitle, Subtitle, SubtitleLine

# maximum and minimum durations
durmax = 90
durmin = 70

input_wav = '01.wav'
input_srt = '01.srt'

s = SrtSubtitle()

s.deserialize(input_srt)

titlovi = s.get_subs()

print(s)

