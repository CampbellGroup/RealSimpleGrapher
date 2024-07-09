from analysis.model import Model, ParameterInfo
import numpy as np

class SineSquared_Ramsey(Model):

    def __init__(self):
        self.parameters = {
            'fringe_freq': ParameterInfo('fringe_freq', 0, self.guess_freq),
            'amplitude': ParameterInfo('amplitude', 1, self.guess_amplitude),
            'phase': ParameterInfo('phase', 2, self.guess_phase),
            'offset': ParameterInfo('offset', 3, self.guess_offset),
            }

    def model(self, x, p):


        f = p[0]
        A = p[1]
        phi = p[2]
        b = p[3]
        return A*np.sin(np.pi*f*x + phi)**2 + b

    def guess_freq(self, x, y):
        time_plot = max(x) - min(x)
        f = 2./time_plot
        return f

    def guess_amplitude(self, x, y):
        return max(y) - min(y)

    def guess_phase(self, x, y):
        return 0

    def guess_offset(self, x, y):
        return min(y)

class RamseyDecay(Model):

	def __init__(self):
		self.parameters = {
			'freq':ParameterInfo('freq', 0, lambda x,y: 10000, vary = True),
            'tau':ParameterInfo('tau', 1, lambda x,y: 1000, vary=True),
            'startfrom': ParameterInfo('startfrom', 2, lambda x,y: 0, vary=True),
            'decayto': ParameterInfo('decayto', 3, lambda x,y: 0.5, vary=False),
            }

	def model(self, x, p):
		t = 1e-6*x
		w = 2*np.pi*p[0]
		tau = 1e-6*p[1]
		startfrom = p[2]
		decayto = p[3]

		return (startfrom-decayto)*np.exp(-t/tau)*np.cos(w*t) + decayto
