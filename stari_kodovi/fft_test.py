#!/usr/bin/python

import scipy
import scipy.fftpack
import pylab
from scipy import pi


t = scipy.linspace(0,120,4000)
acc = lambda t: 10*scipy.cos(2*pi*10*t) #+ 5*scipy.sin(2*pi*8.0*t) #+ 2*scipy.random.random(len(t))

signal = acc(t)

FFT = abs(scipy.fft(signal))
freqs = scipy.fftpack.fftfreq(signal.size, t[1]-t[0])

pylab.subplot(211)
pylab.plot(t, signal)
pylab.subplot(212)
pylab.plot(freqs[0:len(freqs)/2],FFT[0:len(FFT)/2]) #20*scipy.log10(FFT),'x')
pylab.show()

