from scipy import signal
import numpy as np

K = 1
def filter_signal(digital_signal, z, p, k=K) -> []:
    numerator , denominator = signal.zpk2tf(z, p, K)
    filtered_signal = signal.lfilter(numerator, denominator, digital_signal)
    return filtered_signal

def get_frequency_response(z, p, k=K):
    w, h = signal.freqz_zpk(z, p, k)
    magnitude = 20 * np.log10(np.abs(h)) # convert from hz into decibels
    phase = np.unwrap(np.angle(h))   # `np.unwrap` to remove phase discontinuities
    
    if z == [[0j]] or p == [[0j]]:
        magnitude = np.zeros(len(phase))

    return w, magnitude, phase
