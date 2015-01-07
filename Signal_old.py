#!/usr/bin/python3
################################################################################
#
#	Copyright 2014 Stjepan Henc <sthenc@gmail.com>
#
#	Licensed under the Apache License, Version 2.0 (the "License");
#	you may not use this file except in compliance with the License.
#	You may obtain a copy of the License at
#
#		http://www.apache.org/licenses/LICENSE-2.0
#
#	Unless required by applicable law or agreed to in writing, software
#	distributed under the License is distributed on an "AS IS" BASIS,
#	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#	See the License for the specific language governing permissions and
#	limitations under the License.
#
################################################################################

import scipy.io.wavfile as wav
import numpy as np
import scipy.fftpack as sf
import copy
from pprint import pprint
import math as m

class Signal:

	# Data loaders
	def LoadFromFile(self, file):
		self.fs, self.s = wav.read(file)
		self.sLength, self.nChans = self.s.shape

	def LoadWF(self, waveform, fs):
		self.s = waveform
		self.fs = fs
		self.sLength, self.nChans = self.s.shape
	
	def __init__(self, *args):
		if len(args) == 1:
			if type(args[0]) == type(''): # it's a filename
				self.LoadFromFile(args[0])
			elif type(args[0] == type(self)): # copy data from other signal
				self.__dict__ = copy.deepcopy(args[0].__dict__)		
				
		elif len(args) == 2: # args[0] is a signal, args[1] is sample freq.
			self.LoadWF(args(0), args(1))
			
		self.recomputeWeights()

	def cast_precision(self, val):
		if self._precision == 32:
			return np.complex64(val)
		else:
			return np.complex128(val) # or just np.complex()
			
#BEGIN Properties and constraints definitions

	# Signal properties
	_precision = 64
	
	def set_precision(self, val):
		#print('set_precision')
		if not ('_precision' in self.__dict__):
			self._precision = 0
			
		if self._precision != val:
			self._precision = val
			self._s = self.cast_precision(self.s)
			self._S = self.cast_precision(self.S)
			
	def get_precision(self):
		return self._precision

	precision = property(get_precision, set_precision)

	_s = np.array([[0,0],[0,0]], np.float64) 
	
	def set_s(self, val):

		if type(val) != type(np.array([])) or len(val.shape) != 2:
			print('s needs to be 2D ', type(np.array([])))
			print('but is ', type(val), 'shape = ', val.shape)
			exit()
		self._s = val
		self.sLenght, self.nChans = self._s.shape
		
	def get_s(self):
		return self._s
		
	s = property(get_s, set_s)
	
		   
	sLength = 0
	nChans = 0
	weightingFunction = lambda x, y: np.hamming(y)
		
	_fs = 44100

	def set_fs(self, val):
		self._fs = int(val)
		self._nfft = round(self.fs * self.windowLength / 1000)
		self._nfftUtil = round(self.nfft / 2)
		self._overlap = round(self.nfft * self.overlapRatio)
	
	def get_fs(self):
		return self._fs
		
	fs = property(get_fs, set_fs)
	
	#STFT properties
	_S = np.array([[[0,0],[0,0]], [[0,0],[0,0]]], np.float64)
	
	def set_S(self, val):
		self._S = val
		if type(val) != type(np.array([])) or len(val.shape) != 3:
			print('s needs to be 3D ', type(np.array([])))
			print('but is ', type(val), 'shape = ', val.shape)
			exit()
		self.nfft, self.nFrames, self.nChans = val.shape
		self.nfftUtil = round(self.nfft / 2)

	def get_S(self):
		return self._S
	
	S = property(get_S, set_S)
	
	_windowLength = 60
		
	
	def set_windowLength(self, val):
		self._windowLength = int(val)
		self._nfft = round(self.fs * self.windowLength / 1000)
		self._nfftUtil = round(self.nfft / 2)
		self._overlap = round(self.nfft * self.overlapRatio)
		self.recomputeWeights()
		
	def get_windowLength(self):
		return self._windowLength
		
	windowLength = property(get_windowLength, set_windowLength)

	_nfftUtil = 0
	_nfft = 0
	def set_nfft(self, val):
		self._nfft = int(val)
		self.windowLength = (self.nfft * 1000 / self.fs)
		self.overlap = round(self.nfft * self.overlapRatio); 
		self._nfftUtil = self._nfft / 2
		
	def get_nfft(self):
		return self._nfft
		
	nfft = property(get_nfft, set_nfft)
	
	_overlapRatio = 0.5 
	
	def set_overlapRatio(self, val):
		self._overlapRatio = np.float64(val)
		
	def get_overlapRatio(self):
		return self._overlapRatio
	
	overlapRatio = property(get_overlapRatio, set_overlapRatio)

	framesPositions = np.array([], np.float64)
	nFrames = 0
	weightingWindow = np.array([], np.float64)
	overlap = 0 
	
	# Windowing properties -- don' really need to be stored
	# sWin = np.array([], np.float64) 
	# sWeights = np.array([], np.float64)

	def recomputeWeights(self):
		self.weightingWindow = self.weightingFunction(self.nfft)

#END Properties and constraints definitions	   

#XXX heavy lifting

	def STFT(self):
		"""Compute STFT of the signal loaded into s and store result in S"""
		self.recomputeWeights()

		step = self.nfft - self.overlap
		pos = 0
		self.nFrames = m.ceil(self.sLength / step)
		
		
		self._S = np.ndarray([self.nfft, self.nFrames, self.nChans], (np.complex64 if self._precision == 32 else np.complex128) ) 
		
		self._S = np.asfortranarray(self._S)


		print(self.nChans)

		for f in range(0, self.nFrames):
			for c in range(0, self.nChans):
				
				#print (f, c)
				tmp = self.s[f * step : f * step + self.nfft, c] 		
				
				if len(tmp) < self.nfft:							# append zeros for last frame if needed
					tmp = np.append(tmp, [0] * (self.nfft - len(tmp)))
					#print(42, len(tmp))
				
				#print(len(tmp))
				tmpf = sf.fft(tmp * self.weightingWindow)
				self._S[:, f, c] = tmpf

	#def split(self):
	#	""" 
	#	Split s into multiple overlapping frames and return as sWin
	#	"""
	#
	#	step = self._nfft - self._overlap
		
	#def iSTFT(self):
	#	"""Compute iSTFT of the signal in S and store into s"""
		
		
		
		
# DEBUG 
	def print_state(self):
		for k in self.__dict__:
			print('field ', k, 'type ', type(self.__dict__[k]))
			pprint(self.__dict__[k])
			



# TODO something for handling windowfunctions that take both nfft and overlapRatio as input

if __name__ == "__main__":
	a = Signal("./data/britney-short0.wav")
	#fs, ar = wav.read("../matKAM/data/britney-short2.wav")
	a.windowLength = 50
	a.overlapRatio = 0.85	 
	
	a.STFT()
	
	a.print_state()

