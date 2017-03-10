
import numpy as np
import matplotlib.pyplot as plt

V = np.genfromtxt('V.csv',delimiter=",")

A,S,B = np.linalg.svd(V, full_matrices = False)

plot = np.transpose(A[:,:2])

projection = np.dot(plot, V)

projection = np.transpose(projection)

np.savetxt("coords.csv", projection, delimiter=",")