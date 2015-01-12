#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import math
from scipy.interpolate import Rbf

# points = np.array([(1, 1), (2, 4), (3, 1), (9, 3)])

# actually not a_weighting but itu-r 468 instead

points = np.array([ \
(31.5, -29.9), \
(63,   -23.9), \
(100,  -19.8), \
(200,  -13.8), \
(400,  -7.8), \
(800,  -1.9), \
(1000,  0.0), \
(2000,  5.6), \
(3150,  9.0), \
(4000,  10.5), \
(5000,  11.7), \
(6300,  12.2), \
(7100,  12.0), \
(8000,  11.4), \
(9000,  10.1), \
(10000,  8.1), \
(12500,  0.0), \
(14000,  -5.3), \
(16000,  -11.7), \
(20000,  -22.2), \
(25750,  -32.45), \
(31500,  -42.7), \
])

#d_konst = 256000.0
#def func(x, a, b, c):
#    return c * abs((x/d_konst + 0j) ** a) * abs((1 - x/d_konst + 0j) ** b); # beta distribution curve
	
# get x and y vectors
x = points[:,0]
y = [ 10**(tmpy / 20) for tmpy in points[:,1] ]
#y = points[:,1] # for mel variant

#popt, pcov = opt.curve_fit(func, x, y, [1,1,1]) 
 
#f = (lambda x: func(x, *popt) )
# calculate polynomial
#z = np.polyfit(x, y, 6)
#z = np.polyfit(x, y, 3)
#f2 = np.poly1d(z)

# best so far smooth = 0.003, epsilon=default
f2 = Rbf(x, y, smooth=0.3, epsilon=1500)

def f_log(x):
	
	#for i in x:
	#	print(i, " ", end="")
	#print("\n")
	
	#for i in range(0, len(x)):
	#	try:
	#		tmp = math.log10(f2(x[i]))
	#	except ValueError:
	#		print(i, " ", f2(x[i]))
	#
	#print("\n")
	#
	#return []
	return [20*math.log10(f2(i)) for i in x]

def itu_r_468_amplitude_weight():
	return f_log

if __name__ == "__main__":

	f_log = itu_r_468_amplitude_weight()
	# calculate new x's and y's
	x_new = np.linspace(x[0], x[-1], 32000)
	#y_new = f(x_new)
	y2_new = f_log(x_new) # f_log(x_new)
	plt.plot(x,y,'o', x_new, f2(x_new))
	#plt.plot(x,[20*math.log10(t) for t in y],'o', x_new, y2_new)
	
	plt.xlim([x[0]-1, x[-1] + 1 ])
	plt.show()
	
