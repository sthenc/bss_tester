# -*- coding: utf-8 -*-
from __future__ import division
from numpy import sqrt, mean, absolute, real, conj


def rms_flat(a):
    """
    Return the root mean square of all the elements of *a*, flattened out.
    """
    return sqrt(mean(absolute(a)**2))


def rms_fft(spectrum):
    """
    Use Parseval's theorem to find the RMS value of a signal from its fft,
    without wasting time doing an inverse FFT.

    For a signal x, these should produce the same result, to within numerical
    accuracy:

    rms_flat(x) ~= rms_fft(fft(x))
    """
    return rms_flat(spectrum)/sqrt(len(spectrum))


def rms_rfft(spectrum, n=None):
    """
    Use Parseval's theorem to find the RMS value of an even-length signal
    from its rfft, without wasting time doing an inverse real FFT.

    spectrum is produced as spectrum = numpy.fft.rfft(signal)

    For a signal x with an even number of samples, these should produce the
    same result, to within numerical accuracy:

    rms_flat(x) ~= rms_rfft(rfft(x))

    If len(x) is odd, n must be included, or the result will only be
    approximate, due to the ambiguity of rfft for odd lengths.
    """
    if n is None:
        n = (len(spectrum) - 1) * 2
    sq = real(spectrum * conj(spectrum))
    if n % 2:  # odd-length
        mean = (sq[0] + 2*sum(sq[1:])           )/n
    else:  # even-length
        mean = (sq[0] + 2*sum(sq[1:-1]) + sq[-1])/n
    root = sqrt(mean)
    return root/sqrt(n)


if __name__ == "__main__":
    from numpy.random import randn
    from numpy.fft import fft, ifft, rfft, irfft

    n = 17
    x = randn(n)
    X = fft(x)
    rX = rfft(x)

    print(rms_flat(x))
    print(rms_flat(ifft(X)))
    print(rms_fft(X))
    print()

    # Accurate for odd n:
    print(rms_flat(irfft(rX, n)))
    print(rms_rfft(rX, n))
    print()

    # Only approximate for odd n:
    print(rms_flat(irfft(rX)))
    print(rms_rfft(rX))
