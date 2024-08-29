# Fitter class for Sinc

from RealSimpleGrapher.analysis.model import Model, ParameterInfo
import numpy as np


class Sinc(Model):

    def __init__(self):
        self.parameters = {
            "omega": ParameterInfo("omega", 0, self.guess_omega),
            "center": ParameterInfo("center", 1, self.guess_center),
            "offset": ParameterInfo("offset", 2, self.guess_offset),
            "scale": ParameterInfo("scale", 3, self.guess_scale),
        }

    def model(self, x, p):

        omega = p[0]
        center = p[1]
        offset = p[2]
        scale = p[3]
        return (
                scale
                * (omega ** 2 / (omega ** 2 + (center - x) ** 2))
                * np.sin(np.sqrt(omega ** 2 + (center - x) ** 2) * np.pi / (2 * omega)) ** 2
                + offset
        )

    def guess_omega(self, x, y):
        return 20.0

    def guess_amplitude(self, x, y):
        return max(y) - min(y)

    def guess_center(self, x, y):
        return x[np.argmax(y)]

    def guess_offset(self, x, y):
        return min(y)

    def guess_scale(self, x, y):
        return max(y) - min(y)
