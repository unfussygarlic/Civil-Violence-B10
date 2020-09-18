import numpy as np

c = 1
d = 1
e = 0.1
k = 0.01
k_c = 0.8
k_e = 0.99
k_d = 0.7

grievance = 1 - np.exp(-(k_d*(1-d) + k_e*(1-e) + (k_c*c)))
print(grievance)