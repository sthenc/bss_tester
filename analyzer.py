import sys
from scipy.signal import lfilter
import numpy as np
from A_weighting import A_weighting
from scikits.audiolab import wavread  # scipy.io.wavfile can't read 24-bit WAV


def rms_flat(a):  # from matplotlib.mlab
    """
    Return the root mean square of all the elements of *a*, flattened out.
    """
    return np.sqrt(np.mean(np.absolute(a)**2))

if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    filename = 'noise.wav'

x, fs, bits = wavread(filename)
print(filename)
print('Original:   {:+.2f} dB'.format(20*np.log10(rms_flat(x))))
b, a = A_weighting(fs)
y = lfilter(b, a, x)
print('A-weighted: {:+.2f} dB'.format(20*np.log10(rms_flat(y))))
