#!/usr/bin/python

from matplotlib.pylab import *


def f(t):
	return t**2*exp(-t**2)

t = linspace(0, 3, 51)	# 51 points between 0 and 3
y = zeros(len(t)) 		# allocate y with float elements
for i in range(len(t)):
	y[i] = f(t[i])

plot(t, y)
show()
