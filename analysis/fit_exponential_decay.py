#  Fitter class for linear fits

from RealSimpleGrapher.analysis.model import Model, ParameterInfo
import numpy as np


class ExponentialDecay(Model):

    def __init__(self):
        self.parameters = {
            'A': ParameterInfo('A', 0, self.guess_A),
            'tau': ParameterInfo('tau', 1, self.guess_tau),
            'offset': ParameterInfo('offset', 2, self.guess_offset)
            }

    def model(self, t, p):
        A = p[0]
        tau = p[1]
        offset = p[2]
        return A*np.exp(-t/tau) + offset

    def guess_A(self, x, y):
        return y[0]

    def guess_tau(self, x, y):
        return x[int(len(x)/2)]

    def guess_offset(self, x, y):
        return np.min(y)
