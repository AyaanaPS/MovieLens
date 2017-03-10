
import numpy as np
import matplotlib.pyplot as plt

V = np.genfromtxt('V.csv',delimiter=",")

A,S,B = np.linalg.svd(V, full_matrices = False)

# Transpose first 2 columns of A
plot = np.transpose(A[:,:2])
# Dot product with V to get the projection
projection = np.dot(plot, V)

# Transpose projection to write to file in columns
projection = np.transpose(projection)

np.savetxt("coords.csv", projection, delimiter=",")