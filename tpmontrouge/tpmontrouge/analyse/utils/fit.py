from scipy.optimize import curve_fit, fmin
from numpy import pi, sin, exp, array, linspace

def sinusoid(x, offset, amplitude, frequency, phase):
#    offset, amplitude, frequency, phase = p
#    print(offset, amplitude, frequency, phase)
    return offset + amplitude*sin(2*pi*frequency*x+phase)/2

def find_frequency(t, y):
    """ Try to find an initial frequency using a kind of fourier transform """
    y = y - y.mean()
    freq0 = (t.max() - t.min())
    Tfreq = freq0*linspace(1, 20, 101)
    def f_to_optimize(freq):
        res = -abs((y*exp(2J*pi*freq*t)).mean())
        return res
    initial_trials = array(list(map(f_to_optimize, Tfreq)))
    k_opt = initial_trials.argmin()
    return fmin(f_to_optimize, Tfreq[k_opt], disp=0)


def fit_sinusoid(t, y, freq=None, postfix=''):
    """ Fit by a sinusoid. Return a positive amplitude

    Fit the signal y(t) by : 
        offset + amplitude*sin(2*pi*frequency*t-phase)/2
    """
    if freq is None:
#        freq = (t.max() - t.min())*5
        freq = find_frequency(t, y)
    amplitude = y.max() - y.min()
    phase = 0
    offset = y.mean()
    p = offset, amplitude, float(freq), phase
    popt, _ = curve_fit(sinusoid, t, y, p)
    out = dict(zip(['offset', 'amplitude', 'frequency', 'phase'], popt))
    if out['amplitude']<0:
        out['amplitude'] = -out['amplitude']
        out['phase'] = (out['phase'] + pi)%(2*pi)
    return {key+postfix:val for key,val in out.items()}



