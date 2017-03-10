
import numpy as np
import matplotlib.pyplot as plt

V = np.genfromtxt('V.csv',delimiter=",")

A,S,B = np.linalg.svd(V, full_matrices = False)
print(len(B))
B = np.transpose(B)
plot = B[:,:2]
plot = plot / plot.max(axis=0)
print plot

movies = {}
for i,(x,y) in enumerate(plot):
	movies[i+1] = (x,y)
	# print(x,y)

np.savetxt("coords.csv", plot, delimiter=",")