#!/usr/bin/env python
from scipy.fft import fft
import numpy as np

x = np.array([1.0,2.0,1.0,-1.0,1.5])
y = fft(x)
print(y)