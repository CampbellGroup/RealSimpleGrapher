# test script for Lorentzian fits
from model_test import ModelTest
from fit_lorentzian import Lorentzian

test = ModelTest(Lorentzian, "Lorentzian")
true_params = [130.0, 1.0, 5.0, 0.1]
test.generate_data(100, 200, 200, 0.02, true_params)
test.fit()
test.print_results()
test.plot()
